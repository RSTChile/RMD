import os
import time
from typing import Dict, Any, Optional
from .rmd_io import load_json, save_json
from .rmd_hash import sha256_file
from .rmd_trace import Trace
from .rmd_validate import validate_json_file
from .rmd_exceptions import RMDStrictError

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "rmd_config.json")

def load_config(path: str = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    cfg = load_json(path)
    cfg.setdefault("strict_mode", True)
    cfg.setdefault("trace", True)
    cfg.setdefault("outputs_dir", "outputs")
    cfg.setdefault("run_name_prefix", "rmd2_run")
    return cfg

def validate_matrix_file(path: str) -> Dict[str, Any]:
    return validate_json_file(path)

def bootstrap(cfg: Dict[str, Any], repo_root: Optional[str] = None) -> Dict[str, Any]:
    root = repo_root or os.getcwd()
    outputs_dir = os.path.join(root, cfg["outputs_dir"])
    os.makedirs(outputs_dir, exist_ok=True)

    trace = Trace(enabled=bool(cfg.get("trace", True)))
    trace.add("bootstrap_start", {"repo_root": root})

    canon_path = os.path.join(root, cfg["canonical_siglas_source"])
    proto_path = os.path.join(root, cfg["protocol_source"])

    if not os.path.exists(canon_path):
        raise RMDStrictError(f"No existe canonical_siglas_source: {canon_path}")
    if not os.path.exists(proto_path):
        raise RMDStrictError(f"No existe protocol_source: {proto_path}")

    canon_obj = validate_json_file(canon_path)
    proto_obj = validate_json_file(proto_path)

    canon_hash = sha256_file(canon_path)
    proto_hash = sha256_file(proto_path)

    trace.add("sources_loaded", {
        "canonical_siglas_source": cfg["canonical_siglas_source"],
        "protocol_source": cfg["protocol_source"],
        "canonical_sha256": canon_hash,
        "protocol_sha256": proto_hash,
    })

    ctx = {
        "cfg": cfg,
        "repo_root": root,
        "outputs_dir": outputs_dir,
        "trace": trace,
        "sources": {"canonical": canon_obj, "protocol": proto_obj},
        "hashes": {"canonical_sha256": canon_hash, "protocol_sha256": proto_hash},
        "started_at": time.time(),
    }
    trace.add("bootstrap_ok", {"outputs_dir": cfg["outputs_dir"]})
    return ctx

def export_run(ctx: Dict[str, Any], name: Optional[str] = None) -> str:
    cfg = ctx["cfg"]
    run_name = name or f"{cfg.get('run_name_prefix','rmd2_run')}_{int(time.time())}"
    out_dir = os.path.join(ctx["outputs_dir"], run_name)
    os.makedirs(out_dir, exist_ok=True)

    run_meta = {
        "run_name": run_name,
        "strict_mode": bool(cfg.get("strict_mode", True)),
        "trace_enabled": bool(cfg.get("trace", True)),
        "started_at": ctx.get("started_at"),
        "sources": {
            "canonical_siglas_source": cfg.get("canonical_siglas_source"),
            "protocol_source": cfg.get("protocol_source"),
        },
        "hashes": ctx.get("hashes", {}),
    }

    save_json(os.path.join(out_dir, "run_meta.json"), run_meta, indent=2)
    save_json(os.path.join(out_dir, "trace.json"), ctx["trace"].to_dict(), indent=2)
    return out_dir
