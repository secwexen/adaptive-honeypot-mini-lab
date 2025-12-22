import threading
import time
import yaml
import os
from analysis.log_collector import LogCollector
from analysis.pattern_analyzer import PatternAnalyzer
from analysis.decision_engine import DecisionEngine
from integration.siem_connector import SIEMConnector
from integration.alert_system import AlertSystem
from core.ssh_service import SSHFakeService
from core.http_service import HTTPFakeService
from core.ftp_service import FTPFakeService

CONFIG_PATH = os.path.join("config", "settings.yaml")
RULES_PATH = os.path.join("config", "rules.yaml")

def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    settings = load_yaml(CONFIG_PATH)
    rules = load_yaml(RULES_PATH)

    log = LogCollector(settings)
    siem = SIEMConnector(settings, log)
    alert = AlertSystem(settings, log)
    analyzer = PatternAnalyzer(settings, rules, log)
    decision = DecisionEngine(settings, analyzer, siem, alert, log)

    services = {}
    # Initialize services according to settings
    if settings["services"].get("ssh", False):
        services["ssh"] = SSHFakeService(port=settings["ports"]["ssh"], log=log, analyzer=analyzer)
    if settings["services"].get("http", False):
        services["http"] = HTTPFakeService(port=settings["ports"]["http"], log=log, analyzer=analyzer)
    if settings["services"].get("ftp", False):
        services["ftp"] = FTPFakeService(port=settings["ports"]["ftp"], log=log, analyzer=analyzer)

    # Start services in threads
    threads = []
    for name, svc in services.items():
        t = threading.Thread(target=svc.run, name=f"{name}-service", daemon=True)
        t.start()
        threads.append(t)
        log.info("service_start", f"{name} started on port {svc.port}")

    # Start analyzer routine
    analyzer_thread = threading.Thread(target=analyzer.run, name="analyzer", daemon=True)
    analyzer_thread.start()

    # Decision engine routine
    decision_thread = threading.Thread(target=decision.run, name="decision-engine", daemon=True)
    decision_thread.start()

    log.info("system", "Adaptive Honeypot Mini-Lab running")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        log.info("system", "Shutting down honeypot...")

if __name__ == "__main__":
    main()
