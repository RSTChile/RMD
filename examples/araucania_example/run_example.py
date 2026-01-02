import os, sys

HERE = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(HERE, "../.."))
sys.path.insert(0, REPO_ROOT)

from core.rmd_runtime import load_config, bootstrap, validate_matrix_file, export_run

def main():
    cfg = load_config(os.path.join(REPO_ROOT, "core", "rmd_config.json"))
    ctx = bootstrap(cfg, repo_root=REPO_ROOT)

    matrices_dir = os.path.join(REPO_ROOT, "matrices")
    if os.path.isdir(matrices_dir):
        for fn in ["RMD2_Variables-y-Metricas-Completas.json", "RMD2_Protocolo_de_Analisis.json"]:
            p = os.path.join(matrices_dir, fn)
            if os.path.exists(p):
                validate_matrix_file(p)

    out_dir = export_run(ctx, name="araucania_example_bootstrap")
    print(f"OK: bootstrap + export -> {out_dir}")

if __name__ == "__main__":
    main()
