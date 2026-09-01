import json
from pathlib import Path
import pytest

FIXTURES = Path(__file__).parent / "fixtures"


def parse_sse(path: Path) -> dict:
    """Join the streamed `chunk` contents of a Berlin SSE log and parse the JSON payload."""
    parts: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line.startswith("data:"):
            continue
        body = line[5:].strip()
        if not body:
            continue
        try:
            d = json.loads(body)
        except json.JSONDecodeError:
            continue
        if d.get("type") == "chunk":
            parts.append(d.get("content", ""))
    text = "".join(parts).strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(text)


def load_input(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES


@pytest.fixture
def golden43() -> dict:
    return parse_sse(FIXTURES / "tool-response-43.txt")


@pytest.fixture
def input43() -> dict:
    return load_input("sample-input-43.json")


@pytest.fixture
def input94() -> dict:
    return load_input("sample-input-94.json")


@pytest.fixture
def input123() -> dict:
    return load_input("sample-input-123.json")
