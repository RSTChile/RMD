from typing import Dict, Any
from jsonschema import Draft202012Validator
from .rmd_io import load_json
from .rmd_schema import SCHEMA
from .rmd_exceptions import RMDStrictError

_VALIDATOR = Draft202012Validator(SCHEMA)

def validate_json_file(path: str) -> Dict[str, Any]:
    obj = load_json(path)
    errors = sorted(_VALIDATOR.iter_errors(obj), key=lambda e: e.path)
    if errors:
        msg = "; ".join([f"{list(e.path)}: {e.message}" for e in errors[:10]])
        raise RMDStrictError(f"JSON inválido según schema mínimo: {path} :: {msg}")
    return obj
