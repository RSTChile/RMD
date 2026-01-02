## Engine V1 — scripts

Copia estos archivos en tu repo (manteniendo rutas):
- core/engine_v1.py
- tools/run_engine_v1.py
- tools/make_facts_template.py
- examples/araucania_example/facts.araucania.demo.json

### Demo (con venv activo)
python tools/run_engine_v1.py examples/araucania_example/facts.araucania.demo.json demo_v1

Salida:
outputs/demo_v1/
  - run_meta.json
  - trace.json
  - inputs_normalizado.json
  - result_v1.json
