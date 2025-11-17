# 🧩 OS-Simulator

Simulador modular de un sistema operativo en Python. Modela procesos, planificación y gestión básica de recursos con una arquitectura extensible.

## 🧱 Estructura actual del proyecto

```
os-simulator/
├── models/
│   ├── pcb.py
│   ├── process.py
│   ├── process_manager.py
│
├── schedulers/
│   ├── scheduler_base.py
│   ├── fcfs.py
│   ├── round_robin.py        # (Pendiente)
│   ├── sjf.py                # (Pendiente)
│
├── ui/
│   ├── console.py            # Interfaz de consola
│
├── filesystem/               # (Pendiente)
├── utils/
├── tests/
│   ├── test_processes.py
│   ├── processes_example.txt # Archivo de carga
│
├── main.py
└── README.md
```

## ⚙️ Estado del desarrollo

### Gestión básica de procesos

| Módulo | Estado |
|--------|--------|
| PCB | ✅ |
| Process | ✅ |
| ProcessManager | ⚙️ MVP |
| SchedulerBase | ✅ |
| FCFS | ✅ |

### Interfaz de consola

| Elemento | Estado | Resumen |
|----------|--------|---------|
| `main.py` | ✅ | Punto de entrada del simulador. |
| `ui/console.py` | ✅ | Menú interactivo, carga, ejecución y visualización. |
| Carga desde archivo | ✅ | Compatible con formato `pid,arrival,burst,priority,user`. |
| Ejecución FCFS | ✅ | Llama al scheduler y registra el timeline. |
| Resultados | ✅ | Muestra timeline ASCII. |
| Métricas | ✅ | Waiting, turnaround y throughput. |

## 📘 Módulos principales

### 📌 ProcessManager

Gestión básica de colas y creación de procesos. Ahora incluye:

- `load_from_file(path)` para cargar procesos desde TXT.
- Integración con la interfaz de consola.

### 📌 FCFS Scheduler

Ejecución secuencial basada en tiempos de llegada:

- Ordena por arrival time.
- Registra intervalos (start → end).
- Calcula métricas globales.

### 📌 Console UI (`ui/console.py`)

Funcionalidades implementadas:

- Menú interactivo.
- Cargar procesos desde archivo.
- Ejecutar FCFS.
- Mostrar timeline ASCII.
- Mostrar métricas del algoritmo.

**Ejemplo de salida del Timeline:**

```
P1|=====|0->5
P2|===|5->8
P3|========|8->16
```

## 🧪 Pruebas

En `tests/`:

- `test_processes.py`
- `processes_example.txt`: usado para validar la carga de procesos.

**Formato del archivo:**

```
# pid,arrival,burst,priority,user
1,0,5,0,alice
2,1,3,1,bob
3,2,8,0,root
```