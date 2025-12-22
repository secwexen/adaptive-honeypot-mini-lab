from analysis.pattern_analyzer import PatternAnalyzer

def test_pattern_analyzer_counters():
    settings = {}
    rules = {"rules": []}
    class DummyLog:
        def event(self, x): pass
        def info(self, a, b): pass
    pa = PatternAnalyzer(settings, rules, DummyLog())
    pa.bump_counter("ssh_auth_failed", "1.2.3.4")
    assert pa.counters["ssh_auth_failed"]["1.2.3.4"] == 1
