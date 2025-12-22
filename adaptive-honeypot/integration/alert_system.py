import requests

class AlertSystem:
    def __init__(self, settings, log):
        self.settings = settings
        self.log = log
        # You can add email/webhook settings here if needed
        self.webhook = ""

    def send(self, message: str):
        # Minimal: local log. Add webhook if configured.
        self.log.event({"service": "system", "type": "alert", "payload": {"message": message}})
        if self.webhook:
            try:
                requests.post(self.webhook, json={"text": message}, timeout=2)
            except Exception:
                pass
