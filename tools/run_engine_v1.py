import os, sys, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = (HERE / "..").resolve()
sys.path.insert(0, str(REPO_ROOT))

from core.rmd_runtime import load_config, bootstrap, export_run
from core.engine_v1 import run_engine_v1

def main():
    if len(sys.argv) < 2:
        print("Uso: python tools/run_engine_v1.py <facts.json> [run_name]")
        return 2

    facts_path = sys.argv[1]
    run_name = sys.argv[2] if len(sys.argv) >= 3 else f"engine_v1_{int(time.time())}"

    cfg = load_config(str(REPO_ROOT / "core" / "rmd_config.json"))
    ctx = bootstrap(cfg, repo_root=str(REPO_ROOT))

    run_dir = export_run(ctx, name=run_name)
    run_engine_v1(str(REPO_ROOT), cfg, facts_path, run_dir)

    print(f"OK: Engine V1 -> {run_dir}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
