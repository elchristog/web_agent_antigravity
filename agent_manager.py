#!/usr/bin/env python3
"""
Multi-Agent Manager & Factory CLI for Autonomous Web Growth Engines
Permite crear, iniciar, detener y monitorear múltiples agentes autónomos en la misma máquina.
"""

import os
import sys
import json
import shutil
import subprocess
import argparse
from pathlib import Path

BASE_DIR = Path("/home/elchristog")

def get_agent_directories():
    """Retorna todas las carpetas de agentes de la máquina"""
    return [d for d in BASE_DIR.glob("agente_*") if d.is_dir()]

def check_agent_status(agent_dir: Path) -> dict:
    """Obtiene el estado en vivo de un agente"""
    project_name = agent_dir.name
    state_file = agent_dir / "state.json"
    logs_dir = agent_dir / "logs"
    
    # 1. Verificar proceso running analizando working directory de main.py
    pid = None
    try:
        res = subprocess.run(["pgrep", "-f", "python3 main.py"], capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip():
            pids = res.stdout.strip().split("\n")
            for p in pids:
                try:
                    cwd = os.readlink(f"/proc/{p}/cwd")
                    if os.path.realpath(cwd) == os.path.realpath(agent_dir):
                        pid = p
                        break
                except Exception:
                    pass
    except Exception:
        pass

    state_data = {}
    if state_file.exists():
        try:
            state_data = json.loads(state_file.read_text(encoding="utf-8"))
        except Exception:
            pass

    instr = state_data.get("instructions", "")
    domain = state_data.get("domain", "enfermerausa.com") if isinstance(instr, str) else instr.get("target_domain", "Desconocido")
    kpi_score = state_data.get("kpi", {}).get("current_value", "N/A")
    iteration = state_data.get("iteration_count", 0)

    return {
        "name": project_name,
        "path": str(agent_dir),
        "running": pid is not None,
        "pid": pid,
        "domain": domain,
        "kpi_score": kpi_score,
        "iteration": iteration
    }

def sync_network_registry():
    """Sincroniza el registro central de todos los sitios espejo de la red para linkbuilding cruzado"""
    network_file = BASE_DIR / "agents_network.json"
    agents = get_agent_directories()
    network_data = []

    for agent_dir in agents:
        st = check_agent_status(agent_dir)
        domain = st["domain"]
        clean_name = st["name"].replace("agente_", "")
        
        # Etiqueta amigable según el nicho del agente
        label = f"Enfermera en EE.UU. ({domain})"
        if "colombia" in domain or "colombia" in clean_name:
            label = "Enfermeras de Colombia en USA"
        elif "mexico" in domain or "mexico" in clean_name:
            label = "Enfermeras de México en USA"
        elif "hispanas" in domain or "hispanas" in clean_name:
            label = "Comunidad de Enfermeras Hispanas EE.UU."

        network_data.append({
            "name": st["name"],
            "domain": domain,
            "url": f"https://{domain}",
            "label": label,
            "path": str(agent_dir)
        })

    network_file.write_text(json.dumps(network_data, indent=2), encoding="utf-8")
    return network_data

def cmd_status():
    """Muestra el panel en vivo de todos los agentes"""
    sync_network_registry()
    agents = get_agent_directories()
    print("\n" + "=" * 80)
    print("🤖 PANEL DE CONTROL DE AGENTES AUTÓNOMOS (MULTI-AGENT MANAGER)")
    print("=" * 80)
    print(f"{'PROYECTO':<25} | {'ESTADO':<10} | {'PID':<8} | {'DOMINIO':<25} | {'CICLO':<6} | {'KPI SERP'}")
    print("-" * 80)

    for agent_dir in agents:
        st = check_agent_status(agent_dir)
        status_str = "🟢 ACTIVO" if st["running"] else "🔴 DETENIDO"
        pid_str = st["pid"] or "-"
        kpi_str = f"{st['kpi_score']}/100" if isinstance(st["kpi_score"], (int, float)) else str(st["kpi_score"])
        print(f"{st['name']:<25} | {status_str:<10} | {pid_str:<8} | {st['domain']:<25} | #{st['iteration']:<5} | {kpi_str}")

    print("=" * 80 + "\n")

def cmd_create(name: str, domain: str):
    """Crea un nuevo agente clonando la plantilla base"""
    clean_name = name.lower().replace(" ", "_")
    target_dir = BASE_DIR / f"agente_{clean_name}"
    
    if target_dir.exists():
        print(f"❌ Error: El agente 'agente_{clean_name}' ya existe en {target_dir}")
        return

    source_dir = Path("/home/elchristog/agente_antigravity")
    print(f"📦 Creando nuevo agente autónomo para '{domain}' en {target_dir}...")

    # Clonar archivos core del agente
    shutil.copytree(source_dir, target_dir, ignore=shutil.ignore_patterns("node_modules", "dist", ".git", "logs/*.log"))
    
    # Crear carpetas requeridas
    (target_dir / "logs").mkdir(exist_ok=True)

    # Actualizar instruccion en state.json del nuevo agente
    state_file = target_dir / "state.json"
    new_state = {
        "status": "running",
        "iteration_count": 0,
        "kpi": {
            "title": f"Posicionamiento Real en Google SERP ({domain})",
            "current_value": 0.0,
            "target_value": 100.0,
            "unit": "Puntos (Top 1 = 100%)"
        },
        "instructions": f"Optimizar activamente el sitio {domain} para captar clientes y agendar Sesiones Informativas.",
        "history": []
    }
    state_file.write_text(json.dumps(new_state, indent=2), encoding="utf-8")

    print(f"✅ Agente 'agente_{clean_name}' creado con éxito para el dominio '{domain}'.")
    print(f"👉 Para iniciarlo ejecuta: python3 agent_manager.py start {clean_name}")
    sync_network_registry()

def cmd_start(name: str):
    clean_name = name.lower().replace(" ", "_")
    agent_dir = BASE_DIR / f"agente_{clean_name}" if not clean_name.startswith("agente_") else BASE_DIR / clean_name
    
    if not agent_dir.exists():
        print(f"❌ Error: El directorio {agent_dir} no existe.")
        return

    st = check_agent_status(agent_dir)
    if st["running"]:
        print(f"⚠️ El agente '{st['name']}' ya está corriendo con PID {st['pid']}.")
        return

    cmd = f"nohup python3 main.py > logs/main_process.log 2>&1 &"
    subprocess.Popen(cmd, shell=True, cwd=agent_dir)
    print(f"🚀 Agente '{st['name']}' iniciado en segundo plano.")

def cmd_stop(name: str):
    clean_name = name.lower().replace(" ", "_")
    agent_dir = BASE_DIR / f"agente_{clean_name}" if not clean_name.startswith("agente_") else BASE_DIR / clean_name
    st = check_agent_status(agent_dir)
    
    if not st["running"]:
        print(f"⚠️ El agente '{st['name']}' no se encuentra corriendo.")
        return

    try:
        subprocess.run(["kill", st["pid"]])
        print(f"🛑 Agente '{st['name']}' (PID {st['pid']}) detenido con éxito.")
    except Exception as e:
        print(f"❌ Error al detener el agente: {e}")

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("status", help="Muestra el estado de todos los agentes")

    create_p = subparsers.add_parser("create", help="Crea un nuevo agente para un dominio")
    create_p.add_argument("name", help="Nombre del proyecto/agente (ej. clinica_salud)")
    create_p.add_argument("domain", help="Dominio objetivo (ej. clinicasalud.com)")

    start_p = subparsers.add_parser("start", help="Inicia un agente")
    start_p.add_argument("name", help="Nombre del agente")

    stop_p = subparsers.add_parser("stop", help="Detiene un agente")
    stop_p.add_argument("name", help="Nombre del agente")

    args = parser.parse_args()

    if args.command == "status" or not args.command:
        cmd_status()
    elif args.command == "create":
        cmd_create(args.name, args.domain)
    elif args.command == "start":
        cmd_start(args.name)
    elif args.command == "stop":
        cmd_stop(args.name)

if __name__ == "__main__":
    main()
