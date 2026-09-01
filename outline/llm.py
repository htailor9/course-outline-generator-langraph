"""Provider-agnostic structured LLM calls + offline FakeLLM + prompt rendering."""

from __future__ import annotations

import asyncio
import re
import time
from importlib import resources
from typing import TypeVar

from pydantic import BaseModel
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential_jitter,
)

from outline.config import Settings
from outline.schemas import AnnotateOut, ChaptersOut, PartsOut, TitlesOut

T = TypeVar("T", bound=BaseModel)

_RETRYABLE_NAME_MARKERS = (
    "RateLimit",
    "Timeout",
    "APIConnection",
    "ServiceUnavailable",
    "InternalServer",
    "Throttling",
)


def _is_retryable(exc: BaseException) -> bool:
    """Retry only transport-level failures: timeouts, connection errors, and HTTP 429/5xx.
    Anything else (schema/validation errors, auth errors, bad requests) is not retried.
    """
    name = type(exc).__name__
    if any(marker in name for marker in _RETRYABLE_NAME_MARKERS):
        return True
    status = getattr(exc, "status_code", None)
    return isinstance(status, int) and (status == 429 or status >= 500)


def render(name: str, **vars: str) -> tuple[str, str]:
    text = (
        resources.files("outline.prompts")
        .joinpath(f"{name}.md")
        .read_text(encoding="utf-8")
    )
    system, user = text.split("---USER---", 1)
    for k, v in vars.items():
        user = user.replace("{" + k + "}", str(v))
        system = system.replace("{" + k + "}", str(v))
    return system.strip(), user.strip()


def _tokens(s: str) -> int:
    return max(1, len(s) // 4)


class ClaudeCliLLM:
    """Headless `claude -p --json-schema` client — uses the local Claude Code subscription, no API key.

    Provider name: `claude_cli`. Model ids are Claude Code aliases/ids (e.g. `sonnet`, `haiku`, `opus`).
    """

    _DENY = (
        "Bash,Read,Write,Edit,Glob,Grep,WebFetch,WebSearch,Agent,NotebookEdit,TodoWrite"
    )

    def __init__(self, settings: Settings):
        import shutil

        self.settings = settings
        self._exe = shutil.which("claude")
        if not self._exe:
            raise RuntimeError(
                "`claude` CLI not found on PATH; install Claude Code or use another provider"
            )
        self._sem = asyncio.Semaphore(settings.max_concurrency)

    async def _invoke(
        self, model: str, system: str, user: str, schema_json: str
    ) -> dict:
        import json as _json

        # The user prompt goes via STDIN, not argv: Windows CreateProcess caps the command line
        # (~32k chars), which WinError 206'd plan_chapters/titles prompts on 600+ LO runs.
        args = [
            self._exe,
            "-p",
            "--model",
            model,
            "--output-format",
            "json",
            "--json-schema",
            schema_json,
            "--system-prompt",
            system,
            "--allowedTools",
            "StructuredOutput",
            "--disallowedTools",
            self._DENY,
            "--max-turns",
            "3",
        ]
        async with self._sem:
            proc = await asyncio.create_subprocess_exec(
                *args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            try:
                out, err = await asyncio.wait_for(
                    proc.communicate(input=user.encode("utf-8")),
                    timeout=self.settings.llm_timeout_seconds * 3,
                )
            except asyncio.TimeoutError:
                proc.kill()
                raise TimeoutError(f"claude -p timed out for model {model}")
        text = out.decode("utf-8", errors="replace").strip()
        try:
            return _json.loads(text)
        except _json.JSONDecodeError:
            raise RuntimeError(
                f"claude -p returned non-JSON (rc={proc.returncode}): {text[:300]} {err.decode(errors='replace')[:300]}"
            )

    async def call(
        self, role: str, system: str, user: str, schema: type[T]
    ) -> tuple[T, dict]:
        import json as _json

        model = self.settings.models.get(role, self.settings.models["default"])
        schema_json = _json.dumps(schema.model_json_schema())
        t0 = time.perf_counter()
        attempt, parsed, last_err = 0, None, ""
        usage, model_used = {}, model
        while attempt < 2 and parsed is None:
            attempt += 1
            prompt = (
                user
                if attempt == 1
                else f"{user}\n\nYour previous reply did not match the schema: {last_err}. Reply again with valid data."
            )
            res = await self._invoke(model, system, prompt, schema_json)
            usage = res.get("usage", {}) or {}
            model_used = next(iter(res.get("modelUsage", {}) or {model: None}))
            data = res.get("structured_output")
            if data is None and res.get("result"):
                try:
                    data = _json.loads(res["result"])
                except Exception:
                    data = None
            if data is None:
                last_err = "; ".join(res.get("errors") or []) or res.get(
                    "subtype", "no structured_output"
                )
                continue
            try:
                parsed = schema.model_validate(data)
            except Exception as exc:
                last_err = str(exc)[:500]
        if parsed is None:
            raise ValueError(
                f"structured output failed for {schema.__name__}: {last_err}"
            )
        metric = {
            "role": role,
            "model": model_used,
            "prompt_tokens": int(usage.get("input_tokens", 0))
            + int(usage.get("cache_creation_input_tokens", 0))
            + int(usage.get("cache_read_input_tokens", 0)),
            "completion_tokens": int(usage.get("output_tokens", 0)),
            "ms": int((time.perf_counter() - t0) * 1000),
            "attempt": attempt,
            "cost_usd": res.get("total_cost_usd"),
        }
        return parsed, metric


def make_llm(settings: Settings):
    """Provider factory."""
    if settings.provider == "claude_cli":
        return ClaudeCliLLM(settings)
    return LLM(settings)


class LLM:
    """LangChain-backed client. provider in {anthropic, openai, bedrock_converse}."""

    def __init__(self, settings: Settings):
        from langchain.chat_models import init_chat_model

        self.settings = settings
        self._models = {
            role: init_chat_model(
                f"{settings.provider}:{name}",
                temperature=0,
                timeout=settings.llm_timeout_seconds,
            )
            for role, name in settings.models.items()
        }
        self._sem = asyncio.Semaphore(settings.max_concurrency)

    async def call(
        self, role: str, system: str, user: str, schema: type[T]
    ) -> tuple[T, dict]:
        model = self._models.get(role, self._models["default"])
        runnable = model.with_structured_output(schema, include_raw=True)
        messages = [("system", system), ("human", user)]
        t0 = time.perf_counter()
        attempt = 0

        @retry(
            stop=stop_after_attempt(self.settings.transport_retries),
            wait=wait_exponential_jitter(1, 20),
            retry=retry_if_exception(_is_retryable),
            reraise=True,
        )
        async def _invoke(msgs):
            nonlocal attempt
            attempt += 1
            async with self._sem:
                return await runnable.ainvoke(msgs)

        result = await _invoke(messages)
        parsed = result.get("parsed")
        if parsed is None:  # schema failure: one corrective retry
            err = str(result.get("parsing_error"))[:500]
            result = await _invoke(
                messages
                + [
                    (
                        "human",
                        f"Your previous reply did not match the schema: {err}. Reply again with valid data.",
                    )
                ]
            )
            parsed = result.get("parsed")
            if parsed is None:
                err2 = str(result.get("parsing_error"))[:500]
                raise ValueError(
                    f"structured output failed for {schema.__name__}: {err2}"
                )
        usage = getattr(result.get("raw"), "usage_metadata", None) or {}
        metric = {
            "role": role,
            "model": self.settings.models.get(role, self.settings.models["default"]),
            "prompt_tokens": usage.get("input_tokens", _tokens(system + user)),
            "completion_tokens": usage.get("output_tokens", 0),
            "ms": int((time.perf_counter() - t0) * 1000),
            "attempt": attempt,
        }
        return parsed, metric


_ROW = re.compile(r"^\s*([^|]+?)\s*\|\s*(.*)$")


class FakeLLM:
    """Deterministic offline stand-in. Parses pipe rows from `user`; answers per schema."""

    _SKIP_FIRST_COLS = {"skill", "id", "chapter", "rows", "items"}

    def __init__(
        self, drop_ids: set[str] = frozenset(), fail_roles: set[str] = frozenset()
    ):
        self.drop_ids, self.fail_roles = set(drop_ids), set(fail_roles)
        self.calls: list[dict] = []

    @staticmethod
    def _rows(user: str) -> list[list[str]]:
        rows = []
        for line in user.splitlines():
            m = _ROW.match(line)
            if not m or line.lower().startswith(("rows:", "items")):
                continue
            first = m.group(1).strip()
            if ":" in first or first.lower() in FakeLLM._SKIP_FIRST_COLS:
                continue
            rows.append([first] + [c.strip() for c in m.group(2).split("|")])
        return rows

    async def call(
        self, role: str, system: str, user: str, schema: type[T]
    ) -> tuple[T, dict]:
        self.calls.append({"role": role, "user": user})
        if role in self.fail_roles:
            raise RuntimeError(f"fake failure for {role}")
        rows = [r for r in self._rows(user)]
        metric = {
            "role": role,
            "model": "fake",
            "prompt_tokens": _tokens(system + user),
            "completion_tokens": 0,
            "ms": 0,
            "attempt": 1,
        }
        if schema is AnnotateOut:
            items = []
            for r in rows:
                if r[0] in self.drop_ids:
                    continue
                words = re.findall(r"[A-Za-z]+", r[1])
                verb = words[0].lower() if words else "identify"
                skill = (
                    " ".join(w.title() for w in words[1:4] if len(w) > 3)
                    or "General Skill"
                )
                items.append({"id": r[0], "verb": verb, "primary_skill": skill})
            return AnnotateOut.model_validate({"items": items}), metric
        if schema is PartsOut:
            ids = [r[0] for r in rows if r[0] not in self.drop_ids]
            size = 12
            parts = [
                {
                    "part_name": f"Unit {j + 1} Concepts",
                    "ids": ids[j * size : (j + 1) * size],
                }
                for j in range((len(ids) + size - 1) // size)
            ]
            return (
                PartsOut.model_validate(
                    {
                        "parts": parts
                        or [{"part_name": "Unit 1 Concepts", "ids": ids[:1] or ["L1"]}]
                    }
                ),
                metric,
            )
        if schema is ChaptersOut:
            ids = [r[0] for r in rows if r[0] not in self.drop_ids]
            a = [
                {
                    "id": i,
                    "chapter_name": f"Chapter {k // 3 + 1} Topics",
                    "order_rank": k // 3 + 1,
                }
                for k, i in enumerate(ids)
            ]
            return ChaptersOut.model_validate({"assignments": a}), metric
        if schema is TitlesOut:
            ids = [r[1] if len(r) > 2 and r[1].startswith("L") else r[0] for r in rows]
            mods = [
                {"id": i, "title": f"Concept {i} Skills"}
                for i in ids
                if i not in self.drop_ids
            ]
            return TitlesOut.model_validate({"modules": mods}), metric
        raise NotImplementedError(schema)
