import time
import threading
import json
import os
from datetime import datetime

class LogCollector:
    def __init__(self, settings):
        self.settings = settings
        self.level = settings.get("logging", {}).get("level", "INFO")
        self.file = settings.get("logging", {}).get("file", "honeypot.log")
        self.lock = threading.Lock()

    def _write(self, record):
        line = json.dumps(record, ensure_ascii=False)
        with self.lock:
            with open(self.file, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        print(line)

    def info(self, category, message):
        rec = {
            "ts": datetime.utcnow().isoformat() + "Z",
            "level": "INFO",
            "category": category,
            "message": message
        }
        self._write(rec)

    def event(self, payload: dict):
        payload["ts"] = datetime.utcnow().isoformat() + "Z"
        payload["level"] = "EVENT"
        self._write(payload)
