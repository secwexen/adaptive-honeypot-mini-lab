import json
import requests

class SIEMConnector:
    def __init__(self, settings, log):
        self.settings = settings
        self.log = log
        self.enabled = settings.get("siem", {}).get("enabled", False)
        self.endpoint = settings.get("siem", {}).get("endpoint", "")
        self.index = settings.get("siem", {}).get("index", "honeypot-events")
        self.default_tags = settings.get("siem", {}).get("default_tags", [])

    def send(self, event: dict):
        record = {
            "index": self.index,
            "tags": self.default_tags,
            "event": event
        }
        if self.enabled and self.endpoint:
            try:
                requests.post(self.endpoint, json=record, timeout=2)
            except Exception as e:
                # Fallback to local log
                self.log.info("siem_error", f"send failed: {e}")
        # Always log locally
        self.log.event({"service": event.get("service", "unknown"), "type": "siem_forward", "payload": record})
