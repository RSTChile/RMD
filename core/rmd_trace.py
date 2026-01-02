from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional
import time
from .rmd_hash import sha256_json

@dataclass
class TraceEvent:
    ts: float
    kind: str
    payload: Dict[str, Any]
    prev_hash: Optional[str] = None
    hash: Optional[str] = None

class Trace:
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.events: List[TraceEvent] = []
        self._last_hash: Optional[str] = None

    def add(self, kind: str, payload: Dict[str, Any]):
        if not self.enabled:
            return
        ev = TraceEvent(ts=time.time(), kind=kind, payload=payload, prev_hash=self._last_hash)
        ev.hash = sha256_json({"ts": ev.ts, "kind": ev.kind, "payload": ev.payload, "prev": ev.prev_hash})
        self._last_hash = ev.hash
        self.events.append(ev)

    def to_dict(self):
        return {"events": [asdict(e) for e in self.events], "last_hash": self._last_hash}
