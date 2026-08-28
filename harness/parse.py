"""Parse the output contract. Expects a JSON object; malformed responses are logged
with parse_ok=False for review rather than silently dropped."""
from __future__ import annotations
from dataclasses import dataclass
import json, re


@dataclass
class ParseResult:
    verdict: object      # True=attack, False=normal, None=unparseable
    flagged_hours: list
    reasoning: str
    ok: bool


def parse_response(text):
    m = re.search(r"\{.*\}", text or "", re.DOTALL)
    if not m:
        return ParseResult(None, [], "", False)
    try:
        obj = json.loads(m.group(0))
    except Exception:
        return ParseResult(None, [], "", False)
    v = obj.get("verdict")
    verdict = True if v == "attack" else False if v == "normal" else None
    return ParseResult(verdict, obj.get("flagged_hours", []) or [],
                       obj.get("reasoning", "") or "", verdict is not None)
