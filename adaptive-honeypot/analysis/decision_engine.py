import time

class DecisionEngine:
    def __init__(self, settings, analyzer, siem, alert, log):
        self.settings = settings
        self.analyzer = analyzer
        self.siem = siem
        self.alert = alert
        self.log = log
        self._stop = False

    def run(self):
        # Consume analyzer events and act (tag/switch/alert → forward to SIEM/Alert)
        while not self._stop:
            try:
                self._drain_events()
                time.sleep(1)
            except Exception:
                time.sleep(0.2)

    def _drain_events(self):
        # pull a snapshot of recent events
        events = list(self.analyzer.events)
        for evt in events:
            etype = evt.get("type")
            service = evt.get("service", "unknown")
            ip = evt.get("ip", "unknown")

            if etype in ("tag", "switch_request", "alert_request"):
                # forward to SIEM
                self.siem.send({
                    "service": service,
                    "ip": ip,
                    "event_type": etype,
                    "data": evt
                })

                if etype == "alert_request":
                    self.alert.send(f"Alert: {service} suspicious activity from {ip}")
                if etype == "switch_request":
                    to = evt.get("to", "http")
                    self.log.info("decision", f"switch requested to {to} due to activity from {ip}")
                    # Minimal demo: just log the switch. Actual dynamic enabling/disabling
                    # of services would require service lifecycle management hooks.
