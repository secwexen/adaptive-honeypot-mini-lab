from flask import Flask, request
import logging

class HTTPFakeService:
    def __init__(self, port, log, analyzer):
        self.port = port
        self.log = log
        self.analyzer = analyzer
        self.app = Flask("adaptive_honeypot_http")
        self._setup_routes()

    def _setup_routes(self):
        @self.app.before_request
        def before():
            ip = request.remote_addr or "unknown"
            path = request.path
            query = request.query_string.decode(errors="ignore")
            data = request.get_data(as_text=True, parse_form_data=False) or ""
            self.log.event({
                "service": "http",
                "type": "payload",
                "ip": ip,
                "path": path,
                "query": query,
                "payload": data
            })
            # Simple pattern hints
            if "password" in (path + query + data).lower():
                self.analyzer.bump_counter("http_sensitive", ip)

        @self.app.route("/", defaults={"path": ""}, methods=["GET", "POST"])
        @self.app.route("/<path:path>", methods=["GET", "POST"])
        def index(path):
            return "Adaptive Honeypot HTTP Fake Service", 200

    def run(self):
        # Silence flask logs
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        self.app.run(host="0.0.0.0", port=self.port, debug=False, use_reloader=False)
