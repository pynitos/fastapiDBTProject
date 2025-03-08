from dataclasses import dataclass
from pathlib import Path


@dataclass
class LogConfig:
    level: str = "DEBUG"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    render_json_logs: bool = False
    path: Path | None = None
