import json
import time
from datetime import datetime
from pathlib import Path
from config import STATE_FILE, DEFAULT_INTERVAL_SECONDS

DEFAULT_STATE = {
    "kpi": {
        "title": "Progreso General de la Tarea",
        "current_value": 0.0,
        "target_value": 100.0,
        "unit": "%"
    },
    "instructions": "Analizar los archivos del workspace, generar avances periódicos y optimizar el rendimiento del proyecto cada 5 minutos.",
    "status": "running",
    "interval_seconds": DEFAULT_INTERVAL_SECONDS,
    "iteration_count": 0,
    "last_run": None,
    "next_run": None,
    "history": []
}

class StateManager:
    def __init__(self, filepath: Path = STATE_FILE):
        self.filepath = filepath
        self._ensure_state()

    def _ensure_state(self):
        if not self.filepath.exists():
            self.save(DEFAULT_STATE)

    def load(self) -> dict:
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Fusionar con llaves por defecto si faltan
                for key, val in DEFAULT_STATE.items():
                    if key not in data:
                        data[key] = val
                return data
        except Exception:
            return DEFAULT_STATE.copy()

    def save(self, data: dict):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def update_config(self, kpi_title=None, target_value=None, current_value=None, unit=None, instructions=None, interval_seconds=None):
        state = self.load()
        if kpi_title is not None:
            state["kpi"]["title"] = kpi_title
        if target_value is not None:
            state["kpi"]["target_value"] = float(target_value)
        if current_value is not None:
            state["kpi"]["current_value"] = float(current_value)
        if unit is not None:
            state["kpi"]["unit"] = unit
        if instructions is not None:
            state["instructions"] = instructions
        if interval_seconds is not None:
            state["interval_seconds"] = int(interval_seconds)
        self.save(state)
        return state

    def set_status(self, status: str):
        state = self.load()
        state["status"] = status
        self.save(state)

    def add_history_entry(self, thought: str, action: str, log: str, new_kpi_value: float = None):
        state = self.load()
        state["iteration_count"] += 1
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        state["last_run"] = now_str
        
        # Calcular la próxima ejecución
        interval = state.get("interval_seconds", DEFAULT_INTERVAL_SECONDS)
        next_ts = time.time() + interval
        state["next_run"] = datetime.fromtimestamp(next_ts).strftime("%Y-%m-%d %H:%M:%S")

        if new_kpi_value is not None:
            state["kpi"]["current_value"] = min(float(new_kpi_value), float(state["kpi"]["target_value"]))

        entry = {
            "iteration": state["iteration_count"],
            "timestamp": now_str,
            "thought": thought,
            "action": action,
            "kpi_current": state["kpi"]["current_value"],
            "kpi_target": state["kpi"]["target_value"],
            "log": log
        }
        
        # Mantener últimos 100 registros en memoria de estado
        state["history"].insert(0, entry)
        state["history"] = state["history"][:100]
        self.save(state)
        return entry

state_manager = StateManager()
