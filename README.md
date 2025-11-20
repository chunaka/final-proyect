# 🧩 OS-Simulator

Simulador modular de un sistema operativo en Python. Modela procesos, planificación, gestión de recursos y sistema de archivos con una arquitectura extensible.

## 🧱 Estructura actual del proyecto

```
os-simulator/
├── models/
│   ├── __init__.py
│   ├── pcb.py
│   ├── process.py
│   └── process_manager.py
│
├── schedulers/
│   ├── __init__.py
│   ├── scheduler_base.py
│   ├── fcfs.py
│   ├── sjf.py
│   └── round_robin.py        # (Pendiente)
│
├── ui/
│   ├── __init__.py
│   ├── console.py            # Interfaz de consola
│   └── gui.py                # Interfaz gráfica (Pendiente)
│
├── filesystem/
│   ├── __init__.py
│   ├── node.py               # Nodos del sistema de archivos
│   ├── file_system.py        # Sistema de archivos
│   ├── permissions.py        # Gestión de permisos
│   ├── user.py               # Gestión de usuarios
│   └── commands.py           # Comandos del sistema
│
├── utils/
├── tests/
│   ├── test_processes.py
│   └── processes_example.txt # Archivo de carga
│
├── main.py
├── requirements.txt
└── README.md
```

## ⚙️ Estado del desarrollo

### Gestión básica de procesos

| Módulo | Estado |
|--------|--------|
| PCB | ✅ |
| Process | ✅ |
| ProcessManager | ✅ |
| SchedulerBase | ✅ |
| FCFS | ✅ |
| SJF | ✅ |
| Round Robin | ⚙️ (Pendiente) |

### Sistema de archivos

| Módulo | Estado |
|--------|--------|
| Node | ✅ |
| FileSystem | ✅ |
| Permissions | ✅ |
| User | ✅ |
| Commands | ✅ |

### Interfaz de consola

| Elemento | Estado | Resumen |
|----------|--------|------------|
| `main.py` | ✅ | Punto de entrada con selección de scheduler. |
| `ui/console.py` | ✅ | Menú interactivo, carga, ejecución y visualización. |
| `ui/gui.py` | ⚙️ | Interfaz gráfica (Pendiente). |
| Carga desde archivo | ✅ | Compatible con formato `pid,arrival,burst,priority,user`. |
| Ejecución FCFS | ✅ | Llama al scheduler y registra el timeline. |
| Ejecución SJF | ✅ | Selección del trabajo más corto (no preemptivo). |
| Resultados | ✅ | Muestra timeline ASCII. |
| Métricas | ✅ | Waiting, turnaround y throughput. |

## 📘 Módulos principales

### 📌 Main (`main.py`)

Punto de entrada del simulador. Ahora incluye:

- **Selección de scheduler**: Permite elegir entre FCFS y SJF al inicio.
- **Menú interactivo**: Loop principal del simulador con opciones de carga, ejecución y visualización.
- **Integración flexible**: Diseño modular que facilita agregar nuevos schedulers.

### 📌 ProcessManager

Gestión básica de colas y creación de procesos:

- `load_from_file(path)` para cargar procesos desde TXT.
- Integración con la interfaz de consola.
- Gestión de estados de procesos.

### 📌 FCFS Scheduler

Ejecución secuencial basada en tiempos de llegada:

- Ordena por arrival time.
- Registra intervalos (start → end).
- Calcula métricas globales.

### 📌 SJF Scheduler (Shortest Job First)

Ejecución no preemptiva basada en el tiempo de burst más corto:

- Ordena procesos por tiempo de llegada inicial.
- Selecciona el proceso disponible con el burst time más corto.
- Maneja períodos de inactividad cuando no hay procesos disponibles.
- Calcula métricas de rendimiento (waiting time, turnaround time, throughput).

### 📌 Console UI (`ui/console.py`)

Funcionalidades implementadas:

- Menú interactivo.
- Cargar procesos desde archivo.
- Ejecutar scheduler seleccionado (FCFS o SJF).
- Mostrar timeline ASCII.
- Mostrar métricas del algoritmo.

**Ejemplo de salida del Timeline:**

```
P1|=====|0->5
P2|===|5->8
P3|========|8->16
```

### 📌 Sistema de Archivos (`filesystem/`)

Implementación de un sistema de archivos básico:

- **Node**: Estructura de archivo/directorio con metadatos.
- **FileSystem**: Operaciones CRUD sobre archivos y directorios.
- **Permissions**: Sistema de permisos (lectura, escritura, ejecución).
- **User**: Gestión de usuarios y propietarios.
- **Commands**: Comandos del sistema (ls, cd, mkdir, etc.).

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