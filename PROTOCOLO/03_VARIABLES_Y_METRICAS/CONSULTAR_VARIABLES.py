import json
import sys

archivo = "RMD2_Variables-y-Metricas-Completas.json"

with open(archivo, "r", encoding="utf-8") as f:
    data = json.load(f)["data"]

if len(sys.argv) < 2:
    print("Uso: python3 CONSULTAR_VARIABLES.py 'Subcategoría'")
    sys.exit()

busqueda = sys.argv[1].lower()

resultados = []

for v in data:
    subcats = str(v.get("Sub Categorías para Análisis y Gráficos", "")).lower()
    
    if busqueda in subcats:
        resultados.append(v)

print(f"\nVariables encontradas: {len(resultados)}\n")

for v in resultados:
    print(f"{v.get('Sigla')} — {v.get('Nombre')}")
