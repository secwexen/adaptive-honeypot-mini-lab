import socket
import time

class FTPFakeService:
    def __init__(self, port, log, analyzer):
        self.port = port
        self.log = log
        self.analyzer = analyzer
        self._stop = False

    def run(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(("", self.port))
        sock.listen(20)
        while not self._stop:
            try:
                conn, addr = sock.accept()
                ip = addr[0]
                self.log.info("connect", f"ftp connection from {ip}")
                conn.sendall(b"220 Fake FTP Service Ready\r\n")
                conn.settimeout(2)
                try:
                    data = conn.recv(1024)
                except Exception:
                    data = b""
                payload = data.decode(errors="ignore")
                self.log.event({
                    "service": "ftp",
                    "type": "payload",
                    "ip": ip,
                    "payload": payload
                })
                conn.sendall(b"530 Not logged in\r\n")
                conn.close()
            except Exception:
                time.sleep(0.05)
        sock.close()

    def stop(self):
        self._stop = True
