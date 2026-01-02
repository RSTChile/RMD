import hashlib, json

def sha256_bytes(b: bytes) -> str:
    h = hashlib.sha256()
    h.update(b)
    return h.hexdigest()

def sha256_file(path: str) -> str:
    with open(path, "rb") as f:
        return sha256_bytes(f.read())

def sha256_json(obj) -> str:
    b = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(b)
