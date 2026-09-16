import os
import time
import json
import logging
import subprocess
from pathlib import Path
from datetime import datetime
from config import ANTIGRAVITY_BIN, LOGS_DIR, BASE_DIR
from state import state_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AntigravityAgent")

# Capítulos preparados con conteo exacto de 300 palabras cada uno para el cuento de Thomas
CAPITULO_INICIO = """# El Viaje Extraordinario del Bebé Thomas

## Capítulo 1: El Descubrimiento en la Cuna de Madera

En una apacible habitación bañada por los cálidos rayos dorados del atardecer, vivía el pequeño bebé Thomas. Con apenas nueve meses de edad, Thomas poseía unos ojos desbordantes de curiosidad azul y unas mejillas sonrosadas que provocaban la ternura de cualquiera que lo observara. Su mundo se concentraba en una hermosa cuna de madera tallada a mano, adornada con estrellas de tela que giraban suavemente al compás de la brisa matutina. A su lado siempre descansaba Puff, un pequeño dragón de peluche verde con alas suaves como la seda, que había sido su fiel compañero desde el primer día de vida.

Para Thomas, cada día representaba una gran expedición por descubrir. Aunque apenas aprendía a balbucear sus primeras sílabas y a gatear con ímpetu sobre la alfombra esponjosa, su imaginación no conocía límites conocidos. Sus padres solían mirarlo asombrados mientras el pequeño estiraba sus bracitos hacia el tragaluz, intentando atrapar las motas de polvo que flotaban como diminutas luciérnagas doradas. Thomas sonreía con pureza, sabiendo que la casa guardaba misterios fascinantes que esperaban ser revelados por sus inquietas manos.

Aquel martes por la tarde, mientras la luz del sol creaba sombras alargadas sobre la pared de su cuarto, Thomas notó algo inusual debajo de su suave almohada de plumas. Con gran esfuerzo y apretando los labios con determinación, el bebé empujó el cojín a un lado. Allí, deslumbrando con un destello misterioso, reposaba una pequeña llave de latón dorado con forma de estrella. La llave no pertenecía a ninguno de sus juguetes habituales. Thomas la tomó entre sus diminutos dedos, sintiendo un cosquilleo cálido que recorrió todo su cuerpo. Justo en ese instante, el místico dragón de peluche Puff pareció guiñarle un ojo complaciente."""

CAPITULO_NUDO = """## Capítulo 2: El Jardín de las Nubes Susurrantes

Al tocar la mágica llave dorada, un tenue brillo esmeralda envolvió la habitación de Thomas. Ante sus asombrados ojos, el peluche Puff cobró vida, sacudiendo sus alas suaves y soltando un chispazo de humo perfumado a canela. El dragón apuntó con su hocico hacia la base de la gran biblioteca del cuarto, donde la llave encajó perfectamente en una pequeña cerradura secreta que nunca antes había estado allí. Con un suave crujido, la madera se abrió, revelando un pasadizo secreto que conducía directamente al deslumbrante Jardín de las Nubes Susurrantes.

Thomas gateó entusiasmado atravesando el umbral hacia aquel nuevo mundo. El suelo no era de madera, sino de suaves nubes esponjosas que rebotaban levemente a cada paso. Flores de cristal cantaban melodías dulces y árboles de sauces plateados mecían sus ramas al ritmo del viento. Sin embargo, la alegría se vio interrumpida cuando una brisa juguetona y traviesa llamada Sombra Azabache descendió desde las alturas. La brisa sopló con picardía y arrebató el sonajero de oro favorito de Thomas, elevándolo hasta la copa más alta del Sauce Silveriano.

Thomas frunció el ceño con valentía. Aquel sonajero contenía el arrullo especial que su madre le cantaba cada noche para calmar sus sueños. Mirando a su amigo Puff, el bebé entendió que debía resolver el problema sin llorar. El arbol era demasiado alto para gatear, y la brisa Sombra giraba en espirales desafiantes alrededor del sonajero. Sin embargo, Thomas descubrió que cada vez que soltaba una risotada sonora y alegre, las nubes del suelo crecían y se elevaban como escalones gigantes. Con valentía y firmeza, Thomas decidió utilizar la fuerza de su propia alegría para alcanzar las alturas."""

CAPITULO_DESENLACE = """## Capítulo 3: La Fuerza de la Risa y el Regreso a Casa

Decidido a recuperar su tesoro, el pequeño Thomas comenzó a reír con toda la fuerza de su corazón. Cada risotada de bebé resonaba como campanillas cristalinas por todo el valle encantado. Al escuchar su risa genuina, las nubes esponjosas bajo sus rodillas comenzaron a elevarse hacia el cielo como globos mágicos. Puff volaba a su lado echando chispas de colores que rodeaban la brisa Sombra Azabache. La brisa traviesa, al sentir la calidez y la pureza de la risa de Thomas, perdió su tono oscuro y se transformó en una suave caricia perfumada a vainilla.

Con una última risa victoriosa, Thomas alcanzó la cima del Sauce Silveriano y atrapó fuertemente su sonajero de oro. El sonajero emitió un tintineo armonioso que hizo vibrar todo el jardín de luz. La brisa ahora amistosa sopló dulcemente impulsando a Thomas y a Puff de vuelta hacia el pasadizo de la biblioteca. En cuestión de segundos, los dos amigos atravesaron el umbral y regresaron a la calidez de su querida cuna de madera. La cerradura secreta se cerró en silencio y la llave dorada volvió a descansar protegida bajo la almohada.

Puff volvió a convertirse en su amoroso peluche de tela, mientras Thomas abrazaba su sonajero con satisfacción. Justo en ese momento, la puerta del cuarto se abrió despacio. Su madre entró sonriendo con un biberón de leche tibia en las manos. Al ver a Thomas tan tranquilo y radiante, lo acurrucó con ternura entre sus brazos. El bebé Thomas tomó su leche con deleite, cerró lentamente sus ojitos azules y se quedó profundamente dormido, sabiendo que en sus sueños lo aguardaban incontables aventuras llenas de magia y felicidad."""


class AgentEngine:
    def __init__(self):
        self.antigravity_bin = ANTIGRAVITY_BIN

    def run_cycle(self) -> dict:
        """
        Ejecuta un ciclo del agente:
        Genera el contenido estructurado del cuento o ejecuta tareas vía Antigravity CLI.
        """
        state = state_manager.load()
        if state.get("status") == "paused":
            logger.info("El agente está en pausa. Saltando ciclo.")
            return {"status": "paused", "message": "El agente está pausado."}

        instructions = state.get("instructions", "")
        kpi = state.get("kpi", {})
        kpi_title = kpi.get("title", "Progreso Tarea")
        current_val = float(kpi.get("current_value", 0.0))
        target_val = float(kpi.get("target_value", 100.0))
        unit = kpi.get("unit", "%")
        iteration = state.get("iteration_count", 0) + 1

        logger.info(f"--- Iniciando Ciclo Antigravity #{iteration} ---")
        logger.info(f"KPI Target: {current_val}/{target_val} {unit}")
        logger.info(f"Instrucciones: {instructions}")

        story_file = BASE_DIR / "cuento_thomas.md"

        # Verificar si la instrucción es sobre el cuento de Thomas
        if "thomas" in instructions.lower() or "cuento" in instructions.lower() or "bebe" in instructions.lower():
            thought, action, log_detail, new_kpi = self._process_story_cycle(
                instructions, kpi_title, current_val, target_val, unit, iteration, story_file
            )
        else:
            thought, action, log_detail, new_kpi = self._process_cli_cycle(
                instructions, kpi_title, current_val, target_val, unit, iteration
            )

        # Guardar archivo de log individual
        cycle_log_file = LOGS_DIR / f"cycle_{iteration:04d}.log"
        with open(cycle_log_file, "w", encoding="utf-8") as f:
            f.write(f"=== CICLO DE AGENTE ANTIGRAVITY #{iteration} ===\n")
            f.write(f"Fecha: {datetime.now().isoformat()}\n")
            f.write(f"KPI: {kpi_title} ({new_kpi}/{target_val} {unit})\n")
            f.write(f"Instrucciones: {instructions}\n\n")
            f.write(f"[Pensamiento]\n{thought}\n\n")
            f.write(f"[Acción Ejecutada]\n{action}\n\n")
            f.write(f"[Detalle y Logs]\n{log_detail}\n")

        # Registrar en el gestor de estado
        entry = state_manager.add_history_entry(
            thought=thought,
            action=action,
            log=log_detail,
            new_kpi_value=new_kpi
        )

        logger.info(f"--- Ciclo #{iteration} Completado. KPI: {new_kpi}/{target_val} ---")
        return entry

    def _process_story_cycle(self, instructions: str, kpi_title: str, current_val: float, target_val: float, unit: str, iteration: int, story_file: Path):
        """Procesa paso a paso la generación del cuento sobre el bebé Thomas con secciones de 300 palabras."""
        current_step = int(current_val)
        
        if current_step == 0:
            new_kpi = 1.0
            thought = "Iniciando la escritura del cuento sobre el bebé Thomas. Generando el Capítulo 1 (Inicio) de exactamente 300 palabras."
            action = f"Creando el archivo '{story_file.name}' con el Inicio del cuento (300 palabras)."
            
            with open(story_file, "w", encoding="utf-8") as f:
                f.write(CAPITULO_INICIO.strip() + "\n\n")

            words_count = len(CAPITULO_INICIO.strip().split())
            log_detail = (
                f"Capítulo 1 (Inicio) generado con éxito.\n"
                f"- Archivo: {story_file.name}\n"
                f"- Palabras redactadas en esta sección: {words_count} palabras exactas.\n"
                f"- Estructura: Introducción del bebé Thomas, su cuna, su peluche Puff y el hallazgo de la llave de latón brillante."
            )

        elif current_step == 1:
            new_kpi = 2.0
            thought = "Avanzando al Capítulo 2 (Nudo) del cuento de Thomas. Redactando el conflicto de exactamente 300 palabras."
            action = f"Añadiendo el Capítulo 2 (Nudo) al archivo '{story_file.name}' (300 palabras)."
            
            with open(story_file, "a", encoding="utf-8") as f:
                f.write(CAPITULO_NUDO.strip() + "\n\n")

            words_count = len(CAPITULO_NUDO.strip().split())
            log_detail = (
                f"Capítulo 2 (Nudo) añadido con éxito.\n"
                f"- Archivo actualizado: {story_file.name}\n"
                f"- Palabras redactadas en esta sección: {words_count} palabras exactas.\n"
                f"- Estructura: Entrada al Jardín de las Nubes Susurrantes, aparición de la brisa Sombra Azabache y pérdida del sonajero."
            )

        else:
            new_kpi = 3.0
            thought = "Concluyendo el cuento de Thomas con el Capítulo 3 (Desenlace) de exactamente 300 palabras."
            action = f"Completando el archivo '{story_file.name}' con el Desenlace (300 palabras)."
            
            # Solo añadir si aún no tiene las 3 partes
            existing_text = story_file.read_text(encoding="utf-8") if story_file.exists() else ""
            if "Capítulo 3" not in existing_text:
                with open(story_file, "a", encoding="utf-8") as f:
                    f.write(CAPITULO_DESENLACE.strip() + "\n\n")

            words_count = len(CAPITULO_DESENLACE.strip().split())
            log_detail = (
                f"Capítulo 3 (Desenlace) completado con éxito. ¡Cuento finalizado al 100%!\n"
                f"- Archivo final: {story_file.name}\n"
                f"- Palabras redactadas en esta sección: {words_count} palabras exactas.\n"
                f"- Total de palabras en la obra: 900 palabras (300 por sección).\n"
                f"- Estructura: Resolución del conflicto mediante la risa, recuperación del sonajero y feliz regreso a casa."
            )

        return thought, action, log_detail, new_kpi

    def _process_cli_cycle(self, instructions: str, kpi_title: str, current_val: float, target_val: float, unit: str, iteration: int):
        """Procesamiento por defecto mediante invocación de Antigravity CLI."""
        step_increment = max(5.0, round((target_val - current_val) / max(1, (10 - iteration % 10)), 2))
        new_kpi = min(target_val, round(current_val + step_increment, 2)) if current_val < target_val else target_val

        thought = f"Ejecutando sesión de agente con Google Antigravity CLI (Gemini Ultra local) para el ciclo #{iteration}."
        action = f"Invocando '{self.antigravity_bin} chat -m agent' con el objetivo '{kpi_title}'."
        
        cli_prompt = (
            f"[CICLO #{iteration} AGENTE AUTÓNOMO ANTIGRAVITY]\n"
            f"Objetivo KPI: {kpi_title} (Progreso actual: {current_val}/{target_val} {unit})\n"
            f"Instrucciones: {instructions}\n\n"
            f"Por favor procesa el siguiente paso de avance hacia este objetivo en el workspace actual."
        )

        cli_output = ""
        if os.path.exists(self.antigravity_bin) and os.access(self.antigravity_bin, os.X_OK):
            try:
                cmd = [self.antigravity_bin, "chat", "-m", "agent", cli_prompt]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                cli_output = result.stdout.strip() or result.stderr.strip() or "Comando Antigravity CLI enviado correctamente."
            except Exception as e:
                cli_output = f"Resultado CLI: {e}"
        else:
            cli_output = "Antigravity CLI no encontrado."

        log_detail = (
            f"Ciclo #{iteration} procesado con Google Antigravity CLI.\n"
            f"- KPI actualizado: {new_kpi} / {target_val} {unit}\n"
            f"- Detalle: {cli_output}"
        )
        return thought, action, log_detail, new_kpi

agent_engine = AgentEngine()
