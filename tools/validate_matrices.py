import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = (HERE / "..").resolve()
sys.path.insert(0, str(REPO_ROOT))

from core.rmd_runtime import validate_matrix_file

def main():
    matrices = REPO_ROOT / "matrices"
    if not matrices.exists():
        print("No existe carpeta matrices/.")
        return 1
    ok = 0
    bad = 0
    for p in sorted(matrices.glob("*.json")):
        try:
            validate_matrix_file(str(p))
            ok += 1
        except Exception as e:
            bad += 1
            print(f"ERROR {p.name}: {e}")
    print(f"Validación: OK={ok} BAD={bad}")
    return 0 if bad == 0 else 2

if __name__ == "__main__":
    raise SystemExit(main())
