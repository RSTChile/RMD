import os
import time
from typing import Any, Dict, List, Optional

from .rmd_io import load_json, save_json
from .rmd_exceptions import RMDStrictError

def _safe_float(x) -> Optional[float]:
    try:
        if x is None:
            return None
        return float(x)
    except Exception:
        return None

def _clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x

def load_case_facts(path: str) -> Dict[str, Any]:
    obj = load_json(path)
    if not isinstance(obj, dict):
        raise RMDStrictError(f"facts JSON debe ser objeto raíz: {path}")
    obj.setdefault("facts", [])
    if not isinstance(obj["facts"], list):
        raise RMDStrictError(f"facts debe ser lista: {path}")
    return obj

def compute_basic_metrics(facts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Métricas base sin semántica: conteos + agregados numéricos si existen.

    Convención de campos (opcionales por fact):
      - severity: 0..1
      - confidence: 0..1
      - weight: float >= 0 (default 1)
    """
    n = len(facts)
    if n == 0:
        return {
            "facts_count": 0,
            "severity_mean": None,
            "confidence_mean": None,
            "weighted_evidence": 0.0,
        }

    sev_vals: List[float] = []
    conf_vals: List[float] = []
    weighted = 0.0

    for f in facts:
        w = _safe_float(f.get("weight"))
        if w is None:
            w = 1.0
        if w < 0:
            w = 0.0
        weighted += w

        sev = _safe_float(f.get("severity"))
        if sev is not None:
            sev_vals.append(_clamp01(sev))

        conf = _safe_float(f.get("confidence"))
        if conf is not None:
            conf_vals.append(_clamp01(conf))

    sev_mean = (sum(sev_vals) / len(sev_vals)) if sev_vals else None
    conf_mean = (sum(conf_vals) / len(conf_vals)) if conf_vals else None

    return {
        "facts_count": n,
        "severity_mean": sev_mean,
        "confidence_mean": conf_mean,
        "weighted_evidence": weighted,
    }

def compute_indices_v1(base: Dict[str, Any], cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Índices V1 (proxy) controlados por config.

    - IAH: densidad de evidencia = clamp01(log(1+weighted_evidence)/log(1+K))
    - ICS: tensión/severidad = severity_mean (si existe)
    - IGRMD: promedio de (IAH, ICS, confidence_mean) ignorando null

    K configurable: cfg["engine_v1"]["IAH_K"] (default 300)
    """
    import math

    eng = cfg.get("engine_v1", {}) if isinstance(cfg, dict) else {}
    K = float(eng.get("IAH_K", 300))

    we = float(base.get("weighted_evidence") or 0.0)
    denom = math.log(1.0 + K) if K > 0 else 1.0
    iah = _clamp01((math.log(1.0 + we) / denom) if denom else 0.0)

    ics = base.get("severity_mean")
    conf = base.get("confidence_mean")

    parts = [p for p in [iah, ics, conf] if isinstance(p, (int, float))]
    igrmd = (sum(parts) / len(parts)) if parts else None

    return {"IAH": iah, "ICS": ics, "IGRMD": igrmd}

def run_engine_v1(repo_root: str, cfg: Dict[str, Any], facts_path: str, out_dir: str) -> str:
    """Corre Engine V1. Produce:
      - inputs_normalizado.json
      - result_v1.json
    (run_meta.json + trace.json los genera core.export_run)
    """
    os.makedirs(out_dir, exist_ok=True)

    case = load_case_facts(facts_path)
    facts = case.get("facts", [])

    norm = {
        "case": case.get("case"),
        "generated_at": time.time(),
        "facts_count": len(facts),
        "facts": facts,
    }

    base = compute_basic_metrics(facts)
    idx = compute_indices_v1(base, cfg)

    result = {
        "engine": "v1",
        "case": case.get("case"),
        "base": base,
        "indices": idx,
        "notes": [
            "Engine V1 entrega proxies mínimos; no ejecuta fórmulas RMD completas.",
            "Si no hay severity/confidence por hecho, esos agregados quedan null.",
        ],
    }

    save_json(os.path.join(out_dir, "inputs_normalizado.json"), norm, indent=2)
    save_json(os.path.join(out_dir, "result_v1.json"), result, indent=2)
    return out_dir
