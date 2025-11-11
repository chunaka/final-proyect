# 🧩 OS-Simulator

Simulador modular de un sistema operativo educativo, desarrollado en Python.  
El objetivo del proyecto es modelar los componentes fundamentales de un sistema operativo —como procesos, planificación y gestión de recursos— de forma didáctica y extensible.

---

## 🧱 Estructura del proyecto

os-simulator/
├── models/
│ ├── pcb.py # Define el bloque de control de proceso (PCB)
│ ├── process.py # Representación lógica del proceso
│ ├── process_manager.py # Gestor de procesos: colas y cambios de contexto
├── schedulers/ # (Pendiente) Algoritmos de planificación
│ ├── fcfs.py
│ ├── round_robin.py
│ ├── sjf.py
├── filesystem/ # (Pendiente) Simulación de sistema de archivos
├── ui/ # (Pendiente) Consola o interfaz gráfica
├── utils/ # Utilidades y métricas de simulación
├── tests/ # Casos de prueba y validación de módulos
└── README.md

---

## ⚙️ Estado del desarrollo

### ✅ **Sprint 1 — Gestión básica de procesos**

| Módulo | Estado | Descripción |
|--------|---------|-------------|
| `PCB` | ✅ Completado | Contiene toda la información de control del proceso (PID, estado, tiempos, prioridad, etc.). |
| `Process` | ✅ Completado | Representa la lógica de un proceso, interactuando con su PCB. |
| `ProcessManager` | ⚙️ En progreso | Gestiona colas de procesos, creación y cambio de contexto. |

---

## 📘 Clases principales

### **PCB**
Representa el bloque de control de proceso.  
Guarda información sobre el estado, tiempo restante, tiempos de llegada y ejecución, y métricas de planificación.

### **Process**
Capa de abstracción que maneja la lógica de ejecución del proceso.  
Usa internamente un `PCB` para almacenar su información.

### **ProcessManager**
Administra los procesos del sistema, manteniendo las colas de:
- **READY** → procesos listos para ejecutar  
- **BLOCKED** → procesos en espera  
- **TERMINATED** → procesos finalizados  

Permite crear nuevos procesos y realizar transiciones entre estados.

---

## 🧪 Pruebas actuales

Ubicación: `tests/test_processes.py`

```python
procesos_test1 = [
    {"pid": 1, "llegada": 0, "rafaga": 5, "usuario": "usuario1"},
    {"pid": 2, "llegada": 1, "rafaga": 3, "usuario": "usuario2"}
]
