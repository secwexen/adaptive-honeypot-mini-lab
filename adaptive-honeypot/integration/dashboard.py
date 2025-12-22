# Optional minimal dashboard (disabled by default in settings)
from flask import Flask, jsonify
import logging

app = Flask("adaptive_honeypot_dashboard")

@app.route("/")
def index():
    return jsonify({"status": "Dashboard placeholder"}), 200

def run(port=9090):
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)
