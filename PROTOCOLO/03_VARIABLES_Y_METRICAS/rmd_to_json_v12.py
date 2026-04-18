import docx
import json
import re
import unicodedata


def normalize(text):
    if not text:
        return ""
    text = text.strip().lower()
    text = unicodedata.normalize('NFKD', text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text


def is_variable_start(paragraph, next_lines):
    text = paragraph.text.strip()
    style = paragraph.style.name if paragraph.style else ""

    # 🔥 CONDICIÓN 1: estilo correcto
    if "titulo" not in normalize(style):
        return False

    # 🔥 CONDICIÓN 2: patrón numerado (flexible)
    if not re.match(r'^\d+\s*(?:\.\-|\.\s|\-\s)', text):
        return False

    # 🔥 CONDICIÓN 3: señal estructural
    contexto = normalize(" ".join(next_lines[:5]))

    if any(x in contexto for x in [
        "formula",
        "donde",
        "pertinencia",
        "descripcion"
    ]):
        return True

    return False


def extract_id_name(text):
    text = text.strip()

    m = re.match(r'^\d+\s*(?:\.\-|\.\s|\-\s)\s*([A-Z0-9_\-]+)\s*[:\-–]\s*(.+)', text)
    if m:
        return m.group(1), m.group(2)

    m = re.match(r'^\d+\s*(?:\.\-|\.\s|\-\s)\s*(.+)\s+[—\-]\s*([A-Z0-9_\-]+)$', text)
    if m:
        return m.group(2), m.group(1)

    m = re.match(r'^\d+\s*(?:\.\-|\.\s|\-\s)\s*(.+)', text)
    if m:
        return None, m.group(1)

    return None, text


def detect_block(text):
    t = normalize(text)

    if "formula" in t:
        return "formula"
    if "donde" in t:
        return "componentes"
    if "pertinencia" in t:
        return "pertinencia"
    if "descripcion para un lector" in t:
        return "descripcion"
    if "fuentes" in t:
        return "fuentes"

    return None


def parse_docx(path):
    doc = docx.Document(path)

    variables = []
    current = None
    current_block = None

    paragraphs = doc.paragraphs

    for i, p in enumerate(paragraphs):

        text = p.text.strip()
        if not text:
            continue

        next_lines = [
            paragraphs[j].text.strip()
            for j in range(i+1, min(i+6, len(paragraphs)))
            if paragraphs[j].text.strip()
        ]

        if is_variable_start(p, next_lines):

            if current:
                variables.append(current)

            vid, name = extract_id_name(text)

            current = {
                "id": vid,
                "nombre": name,
                "estructura": {
                    "formula": "",
                    "componentes": "",
                    "pertinencia": "",
                    "descripcion": "",
                    "fuentes": "",
                    "otros": ""
                }
            }

            current_block = None
            continue

        if not current:
            continue

        block = detect_block(text)

        if block:
            current_block = block
            continue

        if current_block:
            current["estructura"][current_block] += text + "\n"
        else:
            current["estructura"]["otros"] += text + "\n"

    if current:
        variables.append(current)

    return variables


def clean(variables):
    result = []

    for v in variables:
        estructura = {}

        for k, val in v["estructura"].items():
            if val.strip():
                estructura[k] = val.strip()

        result.append({
            "id": v["id"],
            "nombre": v["nombre"],
            "estructura": estructura
        })

    return result


def main():
    input_file = "RMD_2_Variables_y_METRICAS_COMPLETAS-30-03-2026.docx"
    output_file = "rmd_output_v13.json"

    print("Procesando con parser estructural + estilos (V13)...")

    variables = parse_docx(input_file)
    variables = clean(variables)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump({"variables": variables}, f, ensure_ascii=False, indent=2)

    print(f"Total variables detectadas: {len(variables)}")
    print(f"Archivo generado: {output_file}")


if __name__ == "__main__":
    main()