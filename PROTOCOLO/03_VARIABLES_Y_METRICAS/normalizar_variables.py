import json
import re

INPUT_FILE = "rmd_output_v13.json"
OUTPUT_FILE = "RMD_VARIABLES_NORMALIZADAS.json"

def limpiar_texto(txt):
    if not txt:
        return ""
    return str(txt).strip()

def extraer_sigla_y_nombre(titulo):
    if not titulo:
        return None, None

    # Caso: "IAH — Índice de Ánimo Hostil"
    match = re.match(r"([A-Z0-9\-]+)\s*[—\-:]\s*(.+)", titulo)
    if match:
        return match.group(1).strip(), match.group(2).strip()

    # Caso invertido: "Índice ... — IAH"
    match = re.match(r"(.+)\s*[—\-:]\s*([A-Z0-9\-]+)$", titulo)
    if match:
        return match.group(2).strip(), match.group(1).strip()

    return None, titulo.strip()

def detectar_tipo(variable):
    nombre = (variable.get("nombre") or "").lower()

    if "meta" in nombre or "cos" in nombre:
        return "metavariable"
    if "índice" in nombre or "indice" in nombre:
        return "variable"
    return "métrica"

def separar_bloques(texto):
    bloques = {
        "formula": "",
        "formula_desarrollo": "",
        "componentes": "",
        "descripcion": "",
        "interpretacion": "",
        "coherencia": ""
    }

    if not texto:
        return bloques

    texto = limpiar_texto(texto)

    # Separadores canónicos
    partes = re.split(r"(Fórmula.*?|Donde:|Pertinencia.*?|Descripción para un lector no técnico:)", texto, flags=re.IGNORECASE)

    actual = "descripcion"

    for p in partes:
        p_lower = p.lower()

        if "fórmula" in p_lower:
            actual = "formula"
        elif "donde" in p_lower:
            actual = "componentes"
        elif "pertinencia" in p_lower:
            actual = "coherencia"
        elif "descripción para un lector no técnico" in p_lower:
            actual = "interpretacion"
        else:
            bloques[actual] += " " + p.strip()

    # limpieza final
    for k in bloques:
        bloques[k] = bloques[k].strip()

    return bloques

def normalizar_variable(v, idx):
    titulo = v.get("titulo") or v.get("nombre") or ""

    sigla, nombre = extraer_sigla_y_nombre(titulo)

    texto_completo = ""
    for key in v:
        if isinstance(v[key], str):
            texto_completo += "\n" + v[key]

    bloques = separar_bloques(texto_completo)

    return {
        "id": idx + 1,
        "sigla": sigla,
        "nombre": nombre,
        "tipo": detectar_tipo({"nombre": nombre}),

        "formula": bloques["formula"],
        "formula_desarrollo": bloques["formula_desarrollo"],

        "componentes": bloques["componentes"],
        "descripcion": bloques["descripcion"],
        "interpretacion": bloques["interpretacion"],
        "coherencia": bloques["coherencia"],

        "notas": "",
        "fuente": "docx"
    }

def main():
    print("Cargando archivo...")

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Detectar lista de variables
    if isinstance(data, dict) and "variables" in data:
        variables = data["variables"]
    elif isinstance(data, list):
        variables = data
    else:
        raise Exception("Formato JSON no reconocido")

    print(f"Variables detectadas: {len(variables)}")

    resultado = []

    for i, v in enumerate(variables):
        try:
            normalizada = normalizar_variable(v, i)
            resultado.append(normalizada)
        except Exception as e:
            print(f"Error en variable {i}: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)

    print(f"\n✔ Archivo generado: {OUTPUT_FILE}")
    print(f"✔ Variables normalizadas: {len(resultado)}")

if __name__ == "__main__":
    main()