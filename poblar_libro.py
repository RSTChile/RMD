#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
poblar_libro.py
===============

Vuelca el contenido de los tres .txt del libro RMD 2.0:

    RMD_PARTE1.txt  →  ESTRUCTURA_LIBRO/PARTE_1_BASE/
    RMD_PARTE2.txt  →  ESTRUCTURA_LIBRO/PARTE_2_CASOS/
    RMD_PARTE3.txt  →  ESTRUCTURA_LIBRO/PARTE_3_PROYECCIONES/

en la estructura de carpetas por capítulo / subcapítulo / sub-subcapítulo,
escribiendo el texto de cada nodo en su ``CONTENIDO.md``.

Decisiones de diseño (consensuadas con el usuario):

* Destino      → ``CONTENIDO.md``. NO toca ``SUBCAPITULO.md`` ni ``CAPITULO.md``.
* Granularidad → hasta ``N_M_K_L`` (4 niveles), allí donde el texto los tenga.
* Ruido        → se borran las carpetas sueltas fuera del patrón ``CAP_N/``
                 (p.ej. ``0/``, ``1/``, ``1_5675/``, ``5_1964/``, ``16_2030/``)
                 cuando se pasa la bandera ``--clean-noise``.
* Faltantes    → se crea ``CAP_N/`` y subcarpetas para cualquier nodo
                 detectado en el texto que no tenga carpeta (p.ej. ``CAP_21``).

Modos:
    python3 poblar_libro.py                    # plan (dry-run) por defecto
    python3 poblar_libro.py --apply            # escribe CONTENIDO.md y crea carpetas
    python3 poblar_libro.py --apply --clean-noise   # además borra ruido

Salida:
    poblar_libro.report.json  — resumen completo (cobertura, acciones, warnings)
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ========================= CONFIG =========================

REPO = Path(__file__).resolve().parent
TXT = {
    1: REPO / "RMD_PARTE1.txt",
    2: REPO / "RMD_PARTE2.txt",
    3: REPO / "RMD_PARTE3.txt",
}
ESTR = REPO / "ESTRUCTURA_LIBRO"
PARTES = {
    1: ESTR / "PARTE_1_BASE",
    2: ESTR / "PARTE_2_CASOS",
    3: ESTR / "PARTE_3_PROYECCIONES",
}
CHAPTERS_BY_PARTE: Dict[int, List[int]] = {
    1: list(range(1, 12)),    # 1..11
    2: [12],
    3: list(range(13, 23)),   # 13..22 (incluye 21)
}

# Línea (body) a partir de la cual empieza el texto real en cada .txt
# (antes es índice/portada). Se detecta automáticamente, pero guardamos un
# fallback conservador por si la detección falla.
BODY_START_FALLBACK = {1: 1441, 2: 24, 3: 24}

# ========================= REGEX =========================

# "CAPÍTULO N: TÍTULO"   "Capítulo N — título"   "CAPÍTULO N"
# Nota: intencionalmente NO incluimos "\." como separador porque "Capítulo 14.3:"
# debe tratarse como subcapítulo, no como chapter 14 con título ".3: ...".
CH_HDR = re.compile(
    r"^\s*(?:CAP[IÍ]TULO|Cap[íi]tulo)\s+(\d+)\s*(?:[:\-–—]\s*(.*))?\s*$"
)

# Formato alternativo sin prefijo "CAPÍTULO": "20. CLASES DE CONFLICTO ..."
# (aparece para el cap 20 en PARTE 3). Requerimos título en mayúsculas para
# evitar falsos positivos con listas numeradas tipo "20. Conflicto ...".
CH_HDR_UPPER = re.compile(
    r"^\s*(\d{1,2})\.\s+([A-ZÁÉÍÓÚÑ0-9][A-ZÁÉÍÓÚÑ0-9 ,;:/\-–—\.\(\)]{8,})$"
)

# "N.M Título"  "N.M.K Título"  "N.M.K.L Título"
# Permite prefijo opcional "CAPÍTULO " o "Capítulo "
SUB_HDR = re.compile(
    r"^\s*(?:(?:CAP[IÍ]TULO|Cap[íi]tulo)\s+)?"
    r"(\d+)\.(\d+)(?:\.(\d+))?(?:\.(\d+))?"
    r"[\s:\.\-–—]+(.{3,})$"
)

# Detección de "PARTE N" al inicio de línea — sirve para localizar donde
# arranca el cuerpo (la primera aparición es el índice, la segunda el cuerpo)
PARTE_HDR = re.compile(r"^\s*PARTE\s+(\d+)\b")


# ========================= MODELO =========================

@dataclass
class Node:
    """Nodo jerárquico: capítulo (nivel 1) o subcapítulo (niveles 2–4)."""
    path: Tuple[int, ...]
    title: str
    start_line: int          # índice 0-based en lines
    end_line: Optional[int] = None  # exclusivo
    children: List["Node"] = field(default_factory=list)

    @property
    def level(self) -> int:
        return len(self.path)

    @property
    def dotted(self) -> str:
        return ".".join(str(x) for x in self.path)

    @property
    def folder_name(self) -> str:
        if self.level == 1:
            return f"CAP_{self.path[0]}"
        return "_".join(str(x) for x in self.path)

    @property
    def header_label(self) -> str:
        if self.level == 1:
            return f"CAPÍTULO {self.path[0]}"
        return f"Subcapítulo {self.dotted}"


# ========================= UTILIDADES =========================

def read_lines(path: Path) -> List[str]:
    with path.open("r", encoding="utf-8") as f:
        return f.read().splitlines()


def find_body_start(lines: List[str], parte: int) -> int:
    """Devuelve el índice (0-based) donde empieza el cuerpo del texto.

    Estrategia:
      - Buscamos la 2ª aparición de ``PARTE N`` (la 1ª está en el índice).
      - Si PARTE1 no tiene 2ª aparición evidente, usamos el fallback.
    """
    matches: List[int] = []
    target_parte = parte
    for i, raw in enumerate(lines):
        m = PARTE_HDR.match(raw)
        if m and int(m.group(1)) == target_parte:
            matches.append(i)
    # PARTE 1 aparece muchas veces; usar fallback porque el cuerpo arranca
    # a la altura del primer "CAPÍTULO 1:" mayúscula.
    if parte == 1:
        for i, raw in enumerate(lines):
            if raw.strip().startswith("CAPÍTULO 1:") or raw.strip().startswith(
                "CAPITULO 1:"
            ):
                return max(0, i - 10)
        return BODY_START_FALLBACK[parte]
    # PARTES 2 y 3: la 1ª aparición de "PARTE N" ya es el cuerpo (los .txt
    # arrancan con portada + PARTE).
    if matches:
        return matches[0]
    return BODY_START_FALLBACK[parte]


def is_title_candidate(line: str) -> bool:
    """Descarta líneas que son obvias referencias cruzadas o fragmentos.

    Este filtro se aplica ÚNICAMENTE para el caso de subcapítulos ``SUB_HDR``;
    los capítulos propiamente tales se reconocen con el patrón ``CH_HDR`` que
    ya es suficientemente específico y no necesita este filtro.
    """
    t = line.strip()
    if not t:
        return False
    if len(t) > 220:
        return False
    # referencia cruzada: contiene ")" que cierra "(Capítulo X.Y)" al comienzo
    if ")" in t and "(" not in t[: t.index(")")]:
        return False
    # Si termina con ")." o "):" es casi siempre una referencia cruzada /
    # cita inline: "(Cap. 12.6).", "(ver 4.3):". En cambio un header como
    # "CAPÍTULO 2: ZONAS DE ESPECIACIÓN CULTURAL (ZEC)" también termina en
    # ")" — se permite siempre que exista "(" antes del ")" final.
    if t.endswith(").") or t.endswith("):"):
        return False
    if t.endswith(")") and "(" not in t[: t.rfind(")")]:
        return False
    return True


def looks_like_real_subtitle(title: str) -> bool:
    """Filtra el "título" extraído (tras la numeración) para descartar prosa."""
    t = title.strip()
    if len(t) < 3:
        return False
    # Primera letra debe ser alfabética
    if not t[0].isalpha():
        return False
    # Exigimos que la primera palabra comience con mayúscula o que el título
    # sea muy corto (hasta 6 palabras). Evita "Entre 2021 y 2025, …"
    first = t.split()[0]
    if first[0].islower():
        return False
    # No permitir lo que se ve como oración (> 18 palabras y con verbos
    # conjugados muy genéricos). Heurística liviana:
    if len(t.split()) > 20 and "." in t[:-1]:
        return False
    return True


def merge_multiline_title(lines: List[str], i: int, title: str) -> str:
    """Fusiona un título partido en 2 líneas.

    Ej: 'CAPÍTULO 13: HUMANOS E IA EN EL TABLERO DE GO:' + línea siguiente
        'APLICACIONES DEL RMD 2.0 A HISTORIAS DE CIENCIA FICCIÓN'.
    """
    if not title:
        # a veces el título está íntegro en la línea siguiente
        for j in (i + 1, i + 2):
            if j < len(lines):
                nxt = lines[j].strip()
                if not nxt:
                    continue
                if CH_HDR.match(nxt) or SUB_HDR.match(nxt):
                    break
                if len(nxt) < 140 and nxt[0:1].isupper():
                    return nxt
        return title

    needs_more = title.endswith(":") or title.endswith(",") or title.endswith("—")
    if not needs_more:
        return title
    if i + 1 < len(lines):
        nxt = lines[i + 1].strip()
        if (
            nxt
            and len(nxt) < 160
            and not CH_HDR.match(nxt)
            and not SUB_HDR.match(nxt)
            and (nxt[0].isupper() or nxt[0] in "ÁÉÍÓÚÑáéíóúñ")
        ):
            return title.rstrip(" :—") + " " + nxt
    return title


# ========================= PARSEO =========================

def detect_headers(
    lines: List[str],
    body_start: int,
    valid_chapters: List[int],
) -> List[Node]:
    """Escanea el texto y devuelve la lista de headers en orden."""
    headers: List[Node] = []
    active_chapter: Optional[int] = None
    seen_chapters: set[int] = set()
    # dedup: algunos capítulos tienen al final una "Tabla Resumida" con
    # una lista de subcapítulos (4.1, 4.2, ...) que provoca falsos matches.
    # Conservamos sólo la PRIMERA ocurrencia en el cuerpo (que siempre es
    # el header real, porque el body_start ya excluyó el índice inicial).
    seen_sub_paths: set[Tuple[int, ...]] = set()

    for i in range(body_start, len(lines)):
        raw = lines[i]
        line = raw.strip()
        if not line:
            continue

        # === ¿Capítulo con prefijo "CAPÍTULO"/"Capítulo"? ===
        m = CH_HDR.match(line)
        if m:
            n = int(m.group(1))
            if n in valid_chapters:
                title = (m.group(2) or "").strip()
                title = merge_multiline_title(lines, i, title)
                headers.append(Node((n,), title, i))
                active_chapter = n
                seen_chapters.add(n)
                continue

        # === ¿Capítulo SIN prefijo, formato "N. TÍTULO_EN_MAYÚSCULAS"? ===
        # Sólo se acepta si el número es capítulo válido, aún no visto, y
        # el título está mayoritariamente en mayúsculas (evita listas
        # numeradas "20. Conflicto entre ...").
        m_up = CH_HDR_UPPER.match(line)
        if m_up:
            n = int(m_up.group(1))
            title = m_up.group(2).strip()
            if (
                n in valid_chapters
                and n not in seen_chapters
                and title == title.upper()
                and len(title.split()) >= 3
            ):
                title = merge_multiline_title(lines, i, title)
                headers.append(Node((n,), title, i))
                active_chapter = n
                seen_chapters.add(n)
                continue

        # === ¿Subcapítulo? ===
        if not is_title_candidate(line):
            continue
        m2 = SUB_HDR.match(line)
        if not m2:
            continue
        nums = [
            int(g)
            for g in (m2.group(1), m2.group(2), m2.group(3), m2.group(4))
            if g
        ]
        title = (m2.group(5) or "").strip()
        if not looks_like_real_subtitle(title):
            continue
        # Si el capítulo raíz del subcapítulo coincide con el activo,
        # se acepta. Si es uno que está dentro de ``valid_chapters`` pero
        # todavía no se ha visto, sintetizamos su header de capítulo aquí
        # (útil p.ej. para CAP 14 en PARTE 3, cuyo body empieza con 14.3).
        root = nums[0]
        if root != active_chapter:
            if root in valid_chapters and root not in seen_chapters:
                headers.append(
                    Node((root,), "(Sin encabezado explícito en el texto)", i)
                )
                active_chapter = root
                seen_chapters.add(root)
            else:
                continue
        title = merge_multiline_title(lines, i, title)
        headers.append(Node(tuple(nums), title, i))

    return headers


def close_ranges(headers: List[Node], n_lines: int) -> None:
    """Rellena ``end_line`` de cada header usando el siguiente header como tope.

    Regla: un header cierra cuando aparece OTRO header de nivel ≤ al suyo
    que pertenece al mismo linaje, o bien un capítulo nuevo.
    """
    for idx, h in enumerate(headers):
        end = n_lines
        for j in range(idx + 1, len(headers)):
            nxt = headers[j]
            # cualquier header posterior cuyo "padre" no descienda de h cierra
            if nxt.level == 1:
                end = nxt.start_line
                break
            if nxt.level <= h.level:
                # sibling o superior
                if nxt.path[: h.level - 1] == h.path[: h.level - 1]:
                    end = nxt.start_line
                    break
                # cambio de linaje a nivel superior
                if nxt.level < h.level:
                    end = nxt.start_line
                    break
            # nxt.level > h.level → es descendiente, no cierra
        h.end_line = end


def build_tree(headers: List[Node]) -> List[Node]:
    """Convierte la lista plana en un árbol anidando por prefijo."""
    roots: List[Node] = []
    stack: List[Node] = []  # path-stack
    for h in headers:
        # quitar del stack todo lo que no sea prefijo de h
        while stack and not (
            len(stack[-1].path) < len(h.path)
            and h.path[: len(stack[-1].path)] == stack[-1].path
        ):
            stack.pop()
        if stack:
            stack[-1].children.append(h)
        else:
            roots.append(h)
        stack.append(h)
    return roots


# ========================= RENDERIZADO =========================

def render_content(node: Node, lines: List[str]) -> str:
    """Devuelve el texto a escribir en ``CONTENIDO.md`` de ``node``.

    Estrategia:
      * Si ``node`` tiene hijos → devolvemos sólo el PREÁMBULO
        (entre header de node y el inicio del primer hijo).
      * Si ``node`` no tiene hijos → texto completo del nodo.

    El bloque incluye, arriba, un pequeño front-matter Markdown:

        # CAPÍTULO N — Título      (o)    ## N.M — Título

    seguido del cuerpo (texto plano tal cual del libro, sin re-formateo).
    """
    if node.end_line is None:
        node.end_line = len(lines)
    # slice base del nodo (desde el header incluido hasta end_line exclusivo)
    text_start = node.start_line + 1  # saltar la línea del header
    # Saltar también la línea que fusionamos al título (si aplica)
    if text_start < len(lines):
        maybe_cont = lines[text_start].strip()
        if maybe_cont and maybe_cont in node.title:
            text_start += 1
    # Determinar el tope del cuerpo de este nodo
    if node.children:
        body_end = node.children[0].start_line
    else:
        body_end = node.end_line

    body = "\n".join(lines[text_start:body_end]).strip()

    # header md
    if node.level == 1:
        md_hdr = f"# CAPÍTULO {node.path[0]} — {node.title}".rstrip(" —")
    else:
        md_hdr = f"## {node.dotted} — {node.title}".rstrip(" —")

    parts = [md_hdr, ""]
    if body:
        parts.append(body)
        parts.append("")
    return "\n".join(parts) + "\n"


# ========================= RUIDO =========================

LEGIT_CAP = re.compile(r"^CAP_(\d+)$")
LEGIT_SUB = re.compile(r"^(\d+)(?:_\d+){1,3}$")
LEGIT_FILES = {"CONTENIDO.md", "SUBCAPITULO.md", "CAPITULO.md"}


def is_legit(name: str, parent_chapter: Optional[int] = None) -> bool:
    """¿``name`` es un nombre válido dentro de la estructura?"""
    if name in LEGIT_FILES or name.startswith("."):
        return True
    m = LEGIT_CAP.match(name)
    if m:
        return True
    m2 = LEGIT_SUB.match(name)
    if m2 and parent_chapter is not None:
        return int(name.split("_")[0]) == parent_chapter
    return False


def collect_noise(parte_dir: Path) -> List[Path]:
    """Devuelve rutas (archivos y carpetas) que NO pertenecen a la estructura válida."""
    noise: List[Path] = []
    if not parte_dir.exists():
        return noise
    # 1. directamente hijos de PARTE_*_*/: sólo CAP_N/ y archivos .md
    for child in sorted(parte_dir.iterdir()):
        if child.is_file():
            if child.name not in LEGIT_FILES and not child.name.startswith("."):
                noise.append(child)
            continue
        if LEGIT_CAP.match(child.name):
            # validar interior recursivamente
            ch_n = int(child.name.split("_")[1])
            _walk_cap(child, ch_n, noise)
        else:
            noise.append(child)
    return noise


def _walk_cap(cap_dir: Path, ch_n: int, noise: List[Path]) -> None:
    for child in sorted(cap_dir.iterdir()):
        if child.is_file():
            if child.name not in LEGIT_FILES and not child.name.startswith("."):
                noise.append(child)
            continue
        if is_legit(child.name, parent_chapter=ch_n):
            _walk_cap(child, ch_n, noise)
        else:
            noise.append(child)


# ========================= PIPELINE =========================

def process_parte(parte: int, apply: bool) -> dict:
    """Procesa una Parte completa; devuelve su sección del reporte."""
    txt_path = TXT[parte]
    parte_dir = PARTES[parte]
    if not txt_path.exists():
        return {"error": f"archivo no encontrado: {txt_path}"}

    lines = read_lines(txt_path)
    body_start = find_body_start(lines, parte)
    valid = CHAPTERS_BY_PARTE[parte]
    headers = detect_headers(lines, body_start, valid)
    close_ranges(headers, len(lines))
    tree = build_tree(headers)

    # recolectar datos para reporte
    chapter_nodes = [h for h in headers if h.level == 1]
    seen_chapters = sorted({h.path[0] for h in chapter_nodes})
    missing_chapters = [c for c in valid if c not in seen_chapters]

    actions: List[dict] = []
    written: List[str] = []
    created_dirs: List[str] = []

    def _recurse(node: Node) -> None:
        folder = _node_folder(parte_dir, node)
        if not folder.exists():
            if apply:
                folder.mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(folder.relative_to(ESTR)))
        content = render_content(node, lines)
        target = folder / "CONTENIDO.md"
        if apply:
            target.write_text(content, encoding="utf-8")
        written.append(
            {
                "path": str(target.relative_to(ESTR)),
                "node": node.dotted,
                "title": node.title[:120],
                "chars": len(content),
                "lines": content.count("\n") + 1,
            }
        )
        for c in node.children:
            _recurse(c)

    for root in tree:
        _recurse(root)

    return {
        "parte": parte,
        "txt": str(txt_path.name),
        "body_start_line": body_start + 1,  # humanos cuentan desde 1
        "total_lines": len(lines),
        "chapters_found": seen_chapters,
        "chapters_missing_in_text": missing_chapters,
        "subheaders_found": sum(1 for h in headers if h.level >= 2),
        "written": written,
        "created_dirs": created_dirs,
        "actions": actions,
    }


def _node_folder(parte_dir: Path, node: Node) -> Path:
    parts = [f"CAP_{node.path[0]}"]
    for depth in range(2, node.level + 1):
        parts.append("_".join(str(x) for x in node.path[:depth]))
    return parte_dir.joinpath(*parts)


# ========================= MAIN =========================

def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n")[3],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--apply",
        action="store_true",
        help="escribe los CONTENIDO.md y crea las carpetas (por defecto: dry-run)",
    )
    ap.add_argument(
        "--clean-noise",
        action="store_true",
        help="elimina carpetas/archivos que no encajan en la estructura válida",
    )
    ap.add_argument(
        "--report",
        default=str(REPO / "poblar_libro.report.json"),
        help="ruta del reporte JSON de salida",
    )
    args = ap.parse_args()

    report: dict = {
        "mode": "apply" if args.apply else "plan",
        "clean_noise": bool(args.clean_noise),
        "partes": [],
        "noise": {},
    }

    # === procesar cada parte ===
    for parte in (1, 2, 3):
        rep = process_parte(parte, apply=args.apply)
        report["partes"].append(rep)

    # === ruido ===
    total_noise = 0
    for parte in (1, 2, 3):
        parte_dir = PARTES[parte]
        noise = collect_noise(parte_dir)
        report["noise"][parte_dir.name] = [
            str(p.relative_to(ESTR)) for p in noise
        ]
        total_noise += len(noise)
        if args.clean_noise and args.apply:
            for p in noise:
                if p.is_dir():
                    shutil.rmtree(p)
                else:
                    p.unlink()

    # === resumen ===
    summary = {
        "mode": report["mode"],
        "clean_noise": report["clean_noise"],
        "noise_items": total_noise,
    }
    for p in report["partes"]:
        key = f"PARTE_{p['parte']}"
        summary[key] = {
            "chapters_found": p["chapters_found"],
            "chapters_missing_in_text": p["chapters_missing_in_text"],
            "subheaders_found": p["subheaders_found"],
            "files_written": len(p["written"]),
            "dirs_created": len(p["created_dirs"]),
        }
    report["summary"] = summary

    # === escribir reporte ===
    Path(args.report).write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # stdout: imprimir resumen legible
    print(f"\n== poblar_libro — modo {report['mode'].upper()} ==")
    for p in report["partes"]:
        print(
            f"  PARTE {p['parte']}  caps={p['chapters_found']}  "
            f"subs={p['subheaders_found']}  files={len(p['written'])}  "
            f"nuevas_carpetas={len(p['created_dirs'])}  "
            f"missing_in_text={p['chapters_missing_in_text']}"
        )
    print(f"  Ruido detectado total: {total_noise}")
    if args.clean_noise and args.apply:
        print("  Ruido eliminado ✓")
    elif args.clean_noise:
        print("  (plan: se eliminaría ruido al aplicar)")
    print(f"  Reporte → {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
