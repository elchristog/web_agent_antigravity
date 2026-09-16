import threading
import asyncio
import logging
from config import HOST, PORT
from server import run_server
from scheduler import scheduler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("Main")

def start_scheduler_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    scheduler.is_running = True
    loop.run_until_complete(scheduler._loop())

if __name__ == "__main__":
    print("=" * 65)
    print(" 🚀 AGENTE AUTÓNOMO ANTIGRAVITY INICIADO")
    print(f" 🌐 Dashboard Web en vivo: http://localhost:{PORT}")
    print(" ⏱️  Intervalo de ejecución: Cada 5 minutos (300 segundos)")
    print(" ⚡ Cero dependencias externas requeridas")
    print("=" * 65)

    # Iniciar el scheduler en un hilo de fondo
    scheduler_thread = threading.Thread(target=start_scheduler_thread, daemon=True)
    scheduler_thread.start()

    # Iniciar el servidor web HTTP en el hilo principal
    try:
        run_server(HOST, PORT)
    except KeyboardInterrupt:
        print("\nDeteniendo Agente Antigravity...")
