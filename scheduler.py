import asyncio
import time
import logging
from datetime import datetime
from state import state_manager
from agent_engine import agent_engine

logger = logging.getLogger("AntigravityScheduler")

class AgentScheduler:
    def __init__(self):
        self.is_running = False
        self.task = None
        self._manual_trigger = asyncio.Event()
        self._loop_ref = None

    async def start(self):
        if self.is_running:
            return
        self.is_running = True
        self.task = asyncio.create_task(self._loop())
        logger.info("Scheduler de 2 horas (7200s) iniciado.")

    async def stop(self):
        self.is_running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        logger.info("Scheduler detenido.")

    def trigger_now(self):
        """Dispara una ejecución manual inmediata del agente (thread-safe)."""
        logger.info("Gatillo manual de ejecución recibido.")
        if self._loop_ref and self._loop_ref.is_running():
            self._loop_ref.call_soon_threadsafe(self._manual_trigger.set)
        else:
            self._manual_trigger.set()

    async def _loop(self):
        self._loop_ref = asyncio.get_running_loop()
        
        # Ejecutar un ciclo inicial al arrancar
        await asyncio.sleep(1)
        try:
            agent_engine.run_cycle()
        except Exception as e:
            logger.error(f"Error en ciclo inicial: {e}")

        while self.is_running:
            state = state_manager.load()
            interval = state.get("interval_seconds", 300)
            status = state.get("status", "running")

            if status == "paused":
                await asyncio.sleep(2)
                continue

            # Calcular próxima ejecución
            next_run_ts = time.time() + interval
            next_run_str = datetime.fromtimestamp(next_run_ts).strftime("%Y-%m-%d %H:%M:%S")
            state_manager.save({**state, "next_run": next_run_str})

            # Esperar el intervalo o un gatillo manual thread-safe
            try:
                await asyncio.wait_for(self._wait_interval(interval), timeout=interval)
            except asyncio.TimeoutError:
                pass

            if not self.is_running:
                break

            # Limpiar el evento de disparo manual si se activó
            self._manual_trigger.clear()

            # Ejecutar el ciclo de trabajo
            logger.info("Ejecutando ciclo del agente...")
            try:
                agent_engine.run_cycle()
            except Exception as e:
                logger.error(f"Error durante el ciclo del agente: {e}")

    async def _wait_interval(self, interval: int):
        # Escucha si se activa el manual trigger
        await self._manual_trigger.wait()

scheduler = AgentScheduler()
