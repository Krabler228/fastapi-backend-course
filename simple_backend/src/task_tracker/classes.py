import json
from pathlib import Path
import requests
from settings import JSONBIN_API_KEY, JSONBIN_BIN_ID
from abc import ABC, abstractmethod

BASE = "https://api.jsonbin.io/v3/b"

class BaseStorage(ABC):
    @abstractmethod
    def load(self) -> list[dict]:
        pass
    @abstractmethod
    def save(self, data: list[dict]) -> None:
        pass

class TaskStorage(BaseStorage):
    def __init__(self, path = "tasks.json"):
        self.path = Path(path)
        if not self.path.exists():
            self.save([])
    def load(self):
        with self.path.open("r", encoding="utf-8") as f:
            return json.load(f)
    def save(self, data):
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(data, f,ensure_ascii=False, indent=2)

class RemoteTaskStorage(BaseStorage):
    def __init__(self):
        self.bin_id = JSONBIN_BIN_ID
        self.headers = {"X-Master-Key": JSONBIN_API_KEY, "Content-Type": "application/json"}
    def load(self) -> list[dict]:
        r = requests.get(f"{BASE}/{self.bin_id}/latest", headers=self.headers, timeout=10)
        r.raise_for_status()
        return r.json()["record"]
    def save(self, data: list[dict])->None:
        r = requests.put(f"{BASE}/{JSONBIN_BIN_ID}", headers=self.headers, json=data, timeout=10)
        r.raise_for_status()
