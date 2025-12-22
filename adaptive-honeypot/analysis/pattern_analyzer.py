import re
import time
from collections import defaultdict, deque

class PatternAnalyzer:
    def __init__(self, settings, rules, log):
        self.settings = settings
        self.rules = rules.get("rules", [])
        self.log = log
        self.counters = defaultdict(lambda: defaultdict(int))  # counter_name -> ip -> count
        self.events = deque(maxlen=1000)
        self._stop = False

    def bump_counter(self, name, ip):
        self.counters[name][ip] += 1
        self.events.append({"type": "counter", "name": name, "ip": ip, "count": self.counters[name][ip]})

    def add_event(self, evt):
        self.events.append(evt)

    def run(self):
        # Simple loop for pattern checks
        while not self._stop:
            try:
                self._evaluate_rules()
                time.sleep(1)
            except Exception as e:
                time.sleep(0.1)

    def _evaluate_rules(self):
        # Evaluate counter-based and payload-based rules
        for rule in self.rules:
            match = rule.get("match", {})
            svc = match.get("service")
            mtype = match.get("type")

            if mtype == "auth_failed_count":
                threshold = int(match.get("threshold", 5))
                # window not enforced strictly in this minimal skeleton
                counter_name = "ssh_auth_failed"
                for ip, count in list(self.counters[counter_name].items()):
                    if count >= threshold:
                        self._apply_actions(rule, ip)

            elif mtype == "payload_regex":
                regex = match.get("regex", "")
                if not regex:
                    continue
                r = re.compile(regex, re.IGNORECASE)
                # scan recent events
                for evt in list(self.events):
                    if evt.get("type") == "payload" and evt.get("service") == svc:
                        payload = evt.get("payload", "") + evt.get("path", "") + evt.get("query", "")
                        if r.search(payload or ""):
                            self._apply_actions(rule, evt.get("ip", "unknown"))

            elif mtype == "connect":
                # simplistic: any payload event from the service triggers
                for evt in list(self.events):
                    if evt.get("service") == svc and evt.get("type") == "payload":
                        self._apply_actions(rule, evt.get("ip", "unknown"))

    def _apply_actions(self, rule, ip):
        actions = rule.get("actions", [])
        for a in actions:
            if a.get("type") == "tag":
                self.log.event({"service": rule["match"]["service"], "type": "tag", "ip": ip, "tag": a.get("value")})
            elif a.get("type") == "switch":
                # emit a switch request event consumed by DecisionEngine
                to_service = a.get("to_service")
                self.log.event({"service": rule["match"]["service"], "type": "switch_request", "ip": ip, "to": to_service})
            elif a.get("type") == "alert":
                self.log.event({"service": rule["match"]["service"], "type": "alert_request", "ip": ip})
