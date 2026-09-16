# 📖 GUÍA DE USO: ADMINISTRADOR MULTI-AGENTE (MULTI-AGENT MANAGER)

Esta guía documenta cómo crear, monitorear y gestionar múltiples agentes autónomos de posicionamiento SEO/GEO en la misma máquina utilizando la herramienta `agent_manager.py`.

---

## 🎛️ Comandos Principales (`agent_manager.py`)

Todos los comandos se ejecutan desde la carpeta principal del agente (`/home/elchristog/agente_antigravity`):

```bash
cd /home/elchristog/agente_antigravity
```

### 1. 📊 Ver Panel de Estado en Vivo de Todos los Agentes
Muestra todos los agentes instalados en la máquina, si están activos o detenidos, su PID en Linux, dominio asignado, número de ciclo e indicador KPI de ranking en Google:

```bash
python3 agent_manager.py status
```

---

### 2. 📦 Crear un Nuevo Agente Autónomo para Otro Sitio Web/Dominio
Clona automáticamente la infraestructura completa (Astro SSG, sincronización con Google Cloud Storage, motores SEO/GEO y linkbuilding) en un nuevo directorio aislado (`/home/elchristog/agente_<nombre_proyecto>`):

```bash
python3 agent_manager.py create nombre_proyecto tudominio.com
```

**Ejemplo:**
```bash
python3 agent_manager.py create colombia enfermerascolombiausa.com
```
*Esto creará la carpeta `/home/elchristog/agente_colombia` configurada para `enfermerascolombiausa.com`.*

---

### 3. 🚀 Iniciar un Agente en Segundo Plano
Para poner a correr un agente creado en segundo plano (proceso `nohup` resistente a cierres de terminal):

```bash
python3 agent_manager.py start nombre_proyecto
```

**Ejemplo:**
```bash
python3 agent_manager.py start colombia
```

---

### 4. 🛑 Detener un Agente Específico
Para detener la ejecución continua de un agente en la máquina:

```bash
python3 agent_manager.py stop nombre_proyecto
```

---

## 🌐 Linkbuilding Cruzado Automático entre Sitios Espejo (Multi-Agent PBN Network)

Todos los agentes creados en la misma máquina se detectan e interconectan automáticamente mediante el archivo de registro central (`/home/elchristog/agents_network.json`):

1. **Registro Automático:** Cada vez que ejecutas `agent_manager.py create` o `status`, el sistema registra todos los dominios activos de la máquina.
2. **Inyección Dinámica de Backlinks:** En cada ciclo de ejecución, el motor `NetworkCrossLinkbuilderEngine` de cada agente lee el registro e inyecta en el pie de página (`Footer.astro`) de su sitio web el bloque **"🌐 Red Oficial de Portales Especializados en Enfermería USA"**.
3. **Transferencia de Autoridad de Dominio:** Todos los sitios de la red quedan enlazados entre sí automáticamente, multiplicando el flujo de PageRank y el enlazado recíproco sin necesidad de intervención manual.

---

## 💡 ¿Cómo funciona internamente?

1. **Aislamiento por Directorio:** Cada agente vive en su propia carpeta en `/home/elchristog/agente_<nombre>`.
2. **Sin Conflictos de Recursos:** Cada proceso consume únicamente ~30 MB de memoria RAM y opera en ciclos en suspensión (`sleep`), por lo que tu equipo puede ejecutar decenas de agentes simultáneamente.
3. **Despliegue Independiente:** Cada agente sincroniza sus builds de Astro con su correspondiente Bucket de Google Cloud Storage o servidor de hosting.
