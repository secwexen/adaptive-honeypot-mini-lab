import socket
import threading
import time

class SSHFakeService:
    def __init__(self, port, log, analyzer):
        self.port = port
        self.log = log
        self.analyzer = analyzer
        self._stop = False

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", self.port))
        sock.listen(50)
        banner = b"SSH-2.0-OpenSSH_8.9p1 Fake\r\n"
        while not self._stop:
            try:
                conn, addr = sock.accept()
                ip = addr[0]
                self.log.info("connect", f"ssh connection from {ip}")
                # Send fake SSH banner
                conn.sendall(banner)
                # Read a bit of data
                conn.settimeout(3)
                data = b""
                try:
                    data = conn.recv(1024)
                except Exception:
                    pass
                # Log and analyze
                payload = data.decode(errors="ignore")
                self.log.event({
                    "service": "ssh",
                    "type": "payload",
                    "ip": ip,
                    "payload": payload
                })
                # Simulate auth failure count if payload contains "password"
                if "pass" in payload.lower():
                    self.analyzer.bump_counter("ssh_auth_failed", ip)
                conn.close()
            except Exception as e:
                time.sleep(0.05)
        sock.close()

    def stop(self):
        self._stop = True
