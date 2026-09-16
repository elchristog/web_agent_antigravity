import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def load_env_file(env_path: Path):
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip()
                    if key and key not in os.environ:
                        os.environ[key] = val

# Cargar .env manualmente
load_env_file(BASE_DIR / ".env")

# Ruta al binario oficial de Google Antigravity en el sistema
ANTIGRAVITY_BIN = os.environ.get("ANTIGRAVITY_BIN", "/usr/bin/antigravity")
DEFAULT_INTERVAL_SECONDS = int(os.environ.get("INTERVAL_SECONDS", "7200"))
PORT = int(os.environ.get("PORT", "8000"))
HOST = os.environ.get("HOST", "0.0.0.0")

STATE_FILE = BASE_DIR / "state.json"
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)
