import json
import logging
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from state import state_manager
from scheduler import scheduler

logger = logging.getLogger("AntigravityServer")
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

class AgentRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            template_file = TEMPLATES_DIR / "index.html"
            if template_file.exists():
                self.wfile.write(template_file.read_bytes())
            else:
                self.wfile.write(b"<h1>Dashboard HTML no encontrado</h1>")
        elif self.path == "/api/state":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            state_data = state_manager.load()
            self.wfile.write(json.dumps(state_data, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body_data = {}
        if content_length > 0:
            raw_body = self.rfile.read(content_length)
            try:
                body_data = json.loads(raw_body.decode("utf-8"))
            except Exception:
                pass

        if self.path == "/api/config":
            updated = state_manager.update_config(
                kpi_title=body_data.get("kpi_title"),
                target_value=body_data.get("target_value"),
                current_value=body_data.get("current_value"),
                unit=body_data.get("unit"),
                instructions=body_data.get("instructions"),
                interval_seconds=body_data.get("interval_seconds")
            )
            self.send_json_response({"status": "ok", "state": updated})

        elif self.path == "/api/control/run-now":
            scheduler.trigger_now()
            self.send_json_response({"status": "ok", "message": "Ejecución iniciada."})

        elif self.path == "/api/control/pause":
            state_manager.set_status("paused")
            self.send_json_response({"status": "ok", "message": "Agente pausado."})

        elif self.path == "/api/control/resume":
            state_manager.set_status("running")
            self.send_json_response({"status": "ok", "message": "Agente reanudado."})

        else:
            self.send_response(404)
            self.end_headers()

    def send_json_response(self, data: dict, status_code: int = 200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def log_message(self, format, *args):
        # Suprimir logs verbosos de peticiones HTTP en consola
        return

def run_server(host: str = "0.0.0.0", port: int = 8000):
    server = ThreadingHTTPServer((host, port), AgentRequestHandler)
    logger.info(f"Servidor HTTP iniciado en http://{host}:{port}")
    server.serve_forever()
