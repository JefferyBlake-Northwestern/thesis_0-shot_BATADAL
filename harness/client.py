"""Model-agnostic client interface.

MockClient      -> deterministic, no network, no key: validates the parse/score/log path.
AnthropicClient -> live runs (reads ANTHROPIC_API_KEY; lazy import so the mock dry-run
                   needs neither the SDK nor a key).
GoogleClient    -> stub; fill in before running the Gemini models.
"""
from __future__ import annotations
import time, hashlib
from dataclasses import dataclass


@dataclass
class Completion:
    text: str
    model_version: str
    latency_s: float
    raw: dict


class BaseClient:
    def complete(self, system, user, model_string, temperature) -> Completion:
        raise NotImplementedError


class MockClient(BaseClient):
    """Contract-shaped response derived deterministically from the prompt, so dry-runs
    are stable and exercise the full downstream path."""
    def complete(self, system, user, model_string, temperature):
        h = int(hashlib.sha256(user.encode()).hexdigest(), 16)
        attack = bool(h % 2)
        body = (
            '{"verdict": "%s", "flagged_hours": %s, "reasoning": "MOCK: %s"}'
            % ("attack" if attack else "normal",
               "[0]" if attack else "[]",
               "apparent mass-balance violation" if attack else "within diurnal envelope")
        )
        return Completion(body, f"mock::{model_string}", 0.0, {"mock": True})


class AnthropicClient(BaseClient):
    def __init__(self):
        self._client = None

    def _ensure(self):
        if self._client is None:
            from anthropic import Anthropic   # lazy: not needed for mock dry-run
            self._client = Anthropic()         # reads ANTHROPIC_API_KEY
        return self._client

    def complete(self, system, user, model_string, temperature):
        """`temperature` is accepted for interface compatibility with mock/Google
        clients but not passed to the Anthropic API. SDK 1.0 removed sampling
        params from messages.create()'s signature, and current Opus (4.7/4.8/5)
        rejects any explicit sampling value server-side. See lab notebook
        2026-08-28 for advisor decision."""
        client = self._ensure()
        t0 = time.time()
        resp = client.messages.create(
            model=model_string, max_tokens=1024,
            system=system, messages=[{"role": "user", "content": user}],
        )
        dt = time.time() - t0
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        version = getattr(resp, "model", model_string)   # served version (Ch.4 §4.8.3)
        raw = resp.model_dump() if hasattr(resp, "model_dump") else {}
        return Completion(text, version, dt, raw)


class GoogleClient(BaseClient):
    def complete(self, system, user, model_string, temperature):
        raise NotImplementedError("Google adapter stub -- fill in before running Gemini models.")


def get_client(name):
    return {"mock": MockClient, "anthropic": AnthropicClient, "google": GoogleClient}[name]()
