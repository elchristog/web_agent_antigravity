# 🚀 Agente Autónomo Antigravity

Un agente de inteligencia artificial ejecutable localmente con bucle de ejecución periódico cada 5 minutos, seguimiento de KPI e instrucciones, e integración nativa con **Google Antigravity CLI** y **Gemini Ultra**.

---

## ✨ Características Principales

- ⏱️ **Ejecución Periódica de 5 Minutos**: Scheduler asíncrono que evalúa tareas y métricas de avance cada 300 segundos.
- 🎯 **Seguimiento de KPI**: Monitoreo de metas numéricas o estructurales (ej. avance de tareas, conteo de palabras, archivos procesados).
- 🌐 **Dashboard Web Interactivo**: Interfaz local en `http://localhost:8000` con diseño en modo oscuro (Glassmorphism), temporizador en vivo y consola de logs.
- 🤖 **Integración con Google Antigravity CLI**: Invoca directamente `/usr/bin/antigravity chat -m agent` aprovechando la suscripción local a **Gemini Ultra** sin gastar créditos de API.
- ⚡ **Cero Dependencias Externa Obligatorias**: Desarrollado en Python 3 nativo.

---

## 🛠️ Estructura del Proyecto

```text
├── config.py           # Configuración base (.env)
├── state.py            # Gestor de estado (state.json) y persistencia del historial
├── agent_engine.py     # Motor de ejecución del agente y Google Antigravity CLI
├── scheduler.py        # Programador asíncrono de 5 minutos (thread-safe)
├── server.py           # Servidor HTTP nativo REST API y entrega del Dashboard
├── main.py             # Punto de entrada principal
├── templates/
│   └── index.html      # Dashboard Web responsive con métricas en tiempo real
└── logs/               # Registro individual de archivos de log por ciclo
```

---

## 🚀 Inicio Rápido

1. Clonar el repositorio:
```bash
git clone https://github.com/elchristog/antigravity_agent.git
cd antigravity_agent
```

2. Iniciar el agente:
```bash
python3 main.py
```

3. Abrir el Dashboard en el navegador:
👉 **http://localhost:8000**
