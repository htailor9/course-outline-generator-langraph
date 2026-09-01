"""Settings from config.yaml + overrides."""

from dataclasses import dataclass, field
from pathlib import Path
import yaml


@dataclass
class Settings:
    provider: str = "anthropic"
    models: dict[str, str] = field(
        default_factory=lambda: {"default": "claude-sonnet-4-5"}
    )
    batch_size: int = 30
    max_concurrency: int = 5
    skill_mode_threshold: int = 300
    llm_timeout_seconds: int = 90
    transport_retries: int = 3


def load(path: str | None = None, **overrides) -> Settings:
    data: dict = {}
    p = Path(path) if path else Path("config.yaml")
    if p.exists():
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    data.update({k: v for k, v in overrides.items() if v is not None})
    return Settings(
        **{k: v for k, v in data.items() if k in Settings.__dataclass_fields__}
    )
