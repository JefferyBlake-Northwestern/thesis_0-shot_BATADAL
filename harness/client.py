"""Model-agnostic client interface.

MockClient      -> deterministic, no network, no key: validates the parse/score/log path.
AnthropicClient -> live runs (reads ANTHROPIC_API_KEY; lazy import so the mock dry-run
                   needs neither the SDK nor a key).
GoogleClient    -> Gemini via google-genai SDK; reads GEMINI_API_KEY (or GOOGLE_API_KEY).
XAIClient       -> Grok via OpenAI-compatible endpoint at api.x.ai; reads XAI_API_KEY.

Dependencies (install only what you use):
    pip install anthropic       # AnthropicClient
    pip install google-genai    # GoogleClient
    pip install openai          # XAIClient (uses OpenAI SDK against api.x.ai)
"""
from __future__ import annotations
import os
import time
import hashlib
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
        """`temperature` is accepted for interface compatibility with other
        clients but not passed to the Anthropic API. SDK 1.0 removed sampling
        params from messages.create()'s signature, and current Opus (4.7/4.8/5)
        rejects any explicit sampling value server-side. See lab notebook
        2026-08-28 for advisor decision."""
        client = self._ensure()
        t0 = time.time()
        resp = client.messages.create(
            model=model_string, max_tokens=8192,
            system=system, messages=[{"role": "user", "content": user}],
        )
        dt = time.time() - t0
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        version = getattr(resp, "model", model_string)   # served version (Ch.4 §4.8.3)
        raw = resp.model_dump() if hasattr(resp, "model_dump") else {}
        return Completion(text, version, dt, raw)


class GoogleClient(BaseClient):
    """Gemini via the current google-genai SDK. Unlike Anthropic Opus, Gemini
    accepts an explicit temperature. system_instruction goes in the config, not
    the message list."""
    def __init__(self):
        self._client = None

    def _ensure(self):
        if self._client is None:
            from google import genai
            # genai.Client() reads GEMINI_API_KEY or GOOGLE_API_KEY from env
            self._client = genai.Client()
        return self._client

    def complete(self, system, user, model_string, temperature):
        from google.genai import types
        from google.genai.errors import ServerError
        client = self._ensure()
        t0 = time.time()
        for attempt in range(5):
            try:
                resp = client.models.generate_content(
                    model=model_string,
                    contents=user,
                    config=types.GenerateContentConfig(
                        system_instruction=system,
                        max_output_tokens=8192,
                        temperature=temperature,
                    ),
                )
                break
            except ServerError as e:
                if e.code == 503 and attempt < 4:
                    wait = 2 ** attempt * 5  # 5, 10, 20, 40s
                    time.sleep(wait)
                    continue
                raise
        dt = time.time() - t0
        text = resp.text or ""
        version = getattr(resp, "model_version", model_string)
        try:
            raw = resp.model_dump() if hasattr(resp, "model_dump") else {}
        except Exception:
            raw = {}
        return Completion(text, version, dt, raw)

class XAIClient(BaseClient):
    """Grok via xAI's OpenAI-compatible endpoint. Uses the openai SDK pointed
    at api.x.ai; xAI is fully OpenAI-compatible per their docs. This is more
    stable than the native xai-sdk, which is newer and less predictable."""
    def __init__(self):
        self._client = None

    def _ensure(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(
                api_key=os.getenv("XAI_API_KEY"),
                base_url="https://api.x.ai/v1",
            )
        return self._client

    def complete(self, system, user, model_string, temperature):
        client = self._ensure()
        t0 = time.time()
        resp = client.chat.completions.create(
            model=model_string,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=8192,
            temperature=temperature,
        )
        dt = time.time() - t0
        text = resp.choices[0].message.content or ""
        version = getattr(resp, "model", model_string)
        try:
            raw = resp.model_dump() if hasattr(resp, "model_dump") else {}
        except Exception:
            raw = {}
        return Completion(text, version, dt, raw)

class OpenAIClient(BaseClient):
    """OpenAI's flagship models. Uses the openai SDK against the standard
    api.openai.com endpoint. Reads OPENAI_API_KEY from env."""
    def __init__(self):
        self._client = None

    def _ensure(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI()   # reads OPENAI_API_KEY
        return self._client

    def complete(self, system, user, model_string, temperature):
        client = self._ensure()
        t0 = time.time()
        resp = client.chat.completions.create(
            model=model_string,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=8192,
            temperature=temperature,
        )
        dt = time.time() - t0
        text = resp.choices[0].message.content or ""
        version = getattr(resp, "model", model_string)
        try:
            raw = resp.model_dump() if hasattr(resp, "model_dump") else {}
        except Exception:
            raw = {}
        return Completion(text, version, dt, raw)

def get_client(name):
    return {
        "mock":       MockClient,
        "anthropic":  AnthropicClient,
        "google":     GoogleClient,
        "xai":        XAIClient,
        "openai":     OpenAIClient,
    }[name]()
