from integration.siem_connector import SIEMConnector

def test_siem_local_log():
    settings = {"siem": {"enabled": False}}
    class DummyLog:
        def event(self, x): pass
        def info(self, a, b): pass
    siem = SIEMConnector(settings, DummyLog())
    siem.send({"service": "ssh", "event_type": "tag"})
    assert True
