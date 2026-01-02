import json, sys
from pathlib import Path

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "facts_template.json"
    obj = {
        "case": "NOMBRE_DEL_CASO",
        "facts": [
            {
                "id": "F001",
                "text": "Hecho verificable, sin interpretación.",
                "source": "URL o referencia",
                "date": "YYYY-MM-DD",
                "severity": 0.0,
                "confidence": 1.0,
                "weight": 1.0
            }
        ]
    }
    Path(out).write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: {out}")

if __name__ == "__main__":
    main()
