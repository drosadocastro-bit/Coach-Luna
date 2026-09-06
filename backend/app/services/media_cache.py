import json
from pathlib import Path
from typing import Any


class JsonMediaCache:
    def __init__(self, directory: Path):
        self.directory = directory
        self.directory.mkdir(parents=True, exist_ok=True)
        self.hits = 0
        self.misses = 0

    def _path(self, key: str) -> Path:
        return self.directory / f"{key}.json"

    def get(self, key: str) -> Any | None:
        path = self._path(key)
        if not path.exists():
            self.misses += 1
            return None
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            self.misses += 1
            return None
        self.hits += 1
        return value

    def put(self, key: str, value: Any) -> None:
        self._path(key).write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
