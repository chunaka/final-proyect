# OS Simulator - Operating System Project

Comprehensive operating system simulator implementing process scheduling algorithms and a virtual file system with Unix-style permissions.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Modules](#modules)
  - [Process Scheduling](#process-scheduling)
  - [File System](#file-system)
- [Examples](#examples)
- [Development](#development)

## ✨ Features

### Process Scheduling (Module 1 & 2)
- ✅ **FCFS (First Come First Served)** - Non-preemptive scheduling
- ✅ **SJF (Shortest Job First)** - Non-preemptive scheduling
- ✅ **Round Robin** - Preemptive scheduling with configurable quantum
- ✅ **Context Switch Tracking** - Monitor process state changes
- ✅ **Process Manager** - Centralized process lifecycle management
- ✅ **Performance Metrics** - Turnaround time, waiting time, response time
- ✅ **Timeline Visualization** - Gantt chart display

### File System (Module 3)
- ✅ **Unix-style Permissions** - rwx permissions for owner/group/others
- ✅ **User Management** - Multiple users with UID and groups
- ✅ **Hierarchical Directory Structure** - Tree-based filesystem
- ✅ **18+ Linux Commands** - Full CLI interface
- ✅ **File Operations** - Create, read, write, delete files and directories
- ✅ **Permission Control** - chmod, chown commands
- ✅ **Config File Support** - Load filesystem from configuration file

## 📁 Project Structure

```
os-simulator/
├── models/
│   ├── process.py         # Process class with PCB
│   ├── pcb.py            # Process Control Block
│   └── process_manager.py # Process lifecycle manager
├── schedulers/
│   ├── scheduler_base.py  # Base scheduler class
│   ├── fcfs.py           # FCFS implementation
│   ├── sjf.py            # SJF implementation
│   └── round_robin.py    # Round Robin implementation
├── filesystem/
│   ├── user.py           # User class with UID and groups
│   ├── permissions.py    # Unix-style permissions (rwx)
│   ├── node.py           # Node, File, and Directory classes
│   ├── file_system.py    # FileSystem orchestrator
│   ├── commands.py       # CLI with 18+ commands
│   └── loader.py         # Load filesystem from config file
├── ui/
│   └── console.py        # Console UI for schedulers
├── tests/
│   ├── processes_example.txt     # Example process configuration
│   └── filesystem_example.txt    # Example filesystem configuration
└── main.py               # Main entry point

```

## 🚀 Installation

### Prerequisites
- Python 3.10 or higher

### Setup

1. Clone the repository:
```bash
git clone https://github.com/chunaka/final-proyect.git
cd os-simulator
```

2. Create virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Run the simulator:
```bash
python main.py
```

## 💻 Usage

### Main Menu

When you run `main.py`, you'll see:

```
============================================================
============ SIMULADOR DE SISTEMA OPERATIVO ===============
============================================================

SELECCIONE UN MÓDULO:

  1. Planificación de Procesos (Schedulers)
  2. Sistema de Archivos
  3. Salir

============================================================
```

### Option 1: Process Scheduling

1. Choose a scheduling algorithm (FCFS, SJF, Round Robin)
2. For Round Robin, specify the quantum
3. Load processes from a file (e.g., `tests/processes_example.txt`)
4. Execute the scheduler
5. View results and metrics

### Option 2: File System

1. Choose to load from config file or use demo
2. Use Linux-like commands to interact with the filesystem
3. Type `help` to see all available commands

## 📚 Modules

### Process Scheduling

#### Algorithms Implemented

**FCFS (First Come First Served)**
- Non-preemptive
- Processes executed in order of arrival
- Simple but can cause convoy effect

**SJF (Shortest Job First)**
- Non-preemptive
- Selects process with shortest burst time
- Minimizes average waiting time

**Round Robin**
- Preemptive
- Time quantum-based scheduling
- Fair CPU allocation
- Configurable quantum value

#### Process File Format

```
# pid,arrival,burst,priority,user
1,0,5,0,alice
2,1,3,1,bob
3,2,8,0,root
```

#### Metrics Calculated

- **Turnaround Time**: Total time from arrival to completion
- **Waiting Time**: Time spent in ready queue
- **Response Time**: Time from arrival to first execution
- **Context Switches**: Number of process state changes

### File System

#### Core Classes

**User**
- Username, UID, and groups
- Root user (UID=0) with special privileges

**Permissions**
- Unix-style rwx (read/write/execute)
- Separate permissions for owner/group/others
- Octal notation support (e.g., "644", "755")

**Node (Abstract)**
- Base class for files and directories
- Metadata: owner, permissions, timestamps

**File**
- Text content storage
- Read/write operations with permission checks

**Directory**
- Hierarchical structure with children
- Parent-child relationships
- Path resolution

**FileSystem**
- Orchestrates all operations
- User management
- Navigation (cd, pwd)
- File operations (touch, mkdir, rm, cat, echo)
- Permission management (chmod, chown)

#### Available Commands

| Command | Description |
|---------|-------------|
| `ls [-a] [-l] [path]` | List directory contents |
| `cd [path]` | Change directory |
| `pwd` | Print working directory |
| `mkdir <dir>` | Create directory |
| `touch <file>` | Create empty file |
| `rm [-r] <file>` | Remove file/directory |
| `cat <file>` | Display file content |
| `echo <text> > <file>` | Write to file |
| `echo <text> >> <file>` | Append to file |
| `chmod <perms> <file>` | Change permissions |
| `chown <user> <file>` | Change owner |
| `tree [-L<n>] [path]` | Display directory tree |
| `whoami` | Show current user |
| `su [user]` | Switch user |
| `adduser <user> <uid>` | Add new user (root only) |
| `clear` | Clear screen |
| `help` | Show help |
| `exit` | Exit file system |

#### Filesystem Config File Format

```
# Comments start with #
user,username,uid,group1,group2,...
dir,/path/to/directory,perms,owner
file,/path/to/file.txt,perms,owner,content

# Example:
user,alice,1000,users,developers
dir,/home/alice,755,alice
file,/home/alice/readme.txt,644,alice,Welcome!
```

## 📖 Examples

### Process Scheduling Example

```bash
$ python main.py
# Select option 1 (Schedulers)
# Choose FCFS
# Load file: tests/processes_example.txt
# Option 2: Execute scheduler
# Option 3: View results
# Option 4: View metrics
```

### File System Example

```bash
$ python main.py
# Select option 2 (File System)
# Choose option 2 (Demo)

root@os-sim:/# ls
etc  home  tmp

root@os-sim:/# cd home

root@os-sim:/home# ls
alice  bob

root@os-sim:/home# cd alice

root@os-sim:/home/alice# ls -l
rw-r--r-- alice        36 readme.txt

root@os-sim:/home/alice# cat readme.txt
Welcome to Alice's home directory!

root@os-sim:/home/alice# touch myfile.txt

root@os-sim:/home/alice# echo "Hello World" > myfile.txt

root@os-sim:/home/alice# cat myfile.txt
Hello World

root@os-sim:/home/alice# chmod 600 myfile.txt

root@os-sim:/home/alice# ls -l myfile.txt
rw------- alice        12 myfile.txt

root@os-sim:/home/alice# tree /
/
├── etc/
├── home/
│   ├── alice/
│   │   ├── readme.txt
│   │   └── myfile.txt
│   └── bob/
└── tmp/
```

## 🛠️ Development

### Code Style

- **Documentation**: English docstrings
- **Typing**: Type hints for function signatures
- **Naming**: Descriptive variable and function names
- **Comments**: Minimal, only when necessary

### Architecture

**Process Scheduling**
- `ProcessManager` handles all process lifecycle operations
- `context_switch()` centralizes state transitions
- Schedulers use `ProcessManager` API

**File System**
- Abstract `Node` class for files and directories
- Permission checks at operation level
- Hierarchical tree structure with parent pointers

### Testing

Manual testing workflows:
1. Process scheduling with different algorithms
2. File system operations with different users
3. Permission enforcement
4. Edge cases (empty directories, permission denied, etc.)

## 📝 Implementation Status

### Module 1: Process Management
- ✅ Process class with PCB
- ✅ ProcessManager with context switching
- ✅ Process states (NEW, READY, RUNNING, TERMINATED)

### Module 2: Scheduling Algorithms
- ✅ FCFS (First Come First Served)
**SJF (Shortest Job First)**
- Non-preemptive
- Selects process with shortest burst time
- Minimizes average waiting time

**Round Robin**
- Preemptive
- Time quantum-based scheduling
- Fair CPU allocation
- Configurable quantum value

#### Process File Format

```
# pid,arrival,burst,priority,user
1,0,5,0,alice
2,1,3,1,bob
3,2,8,0,root
```

#### Metrics Calculated

- **Turnaround Time**: Total time from arrival to completion
- **Waiting Time**: Time spent in ready queue
- **Response Time**: Time from arrival to first execution
- **Context Switches**: Number of process state changes

### File System

#### Core Classes

**User**
- Username, UID, and groups
- Root user (UID=0) with special privileges

**Permissions**
- Unix-style rwx (read/write/execute)
- Separate permissions for owner/group/others
- Octal notation support (e.g., "644", "755")

**Node (Abstract)**
- Base class for files and directories
- Metadata: owner, permissions, timestamps

**File**
- Text content storage
- Read/write operations with permission checks

**Directory**
- Hierarchical structure with children
- Parent-child relationships
- Path resolution

**FileSystem**
- Orchestrates all operations
- User management
- Navigation (cd, pwd)
- File operations (touch, mkdir, rm, cat, echo)
- Permission management (chmod, chown)

#### Available Commands

| Command | Description |
|---------|-------------|
| `ls [-a] [-l] [path]` | List directory contents |
| `cd [path]` | Change directory |
| `pwd` | Print working directory |
| `mkdir <dir>` | Create directory |
| `touch <file>` | Create empty file |
| `rm [-r] <file>` | Remove file/directory |
| `cat <file>` | Display file content |
| `echo <text> > <file>` | Write to file |
| `echo <text> >> <file>` | Append to file |
| `chmod <perms> <file>` | Change permissions |
| `chown <user> <file>` | Change owner |
| `tree [-L<n>] [path]` | Display directory tree |
| `whoami` | Show current user |
| `su [user]` | Switch user |
| `adduser <user> <uid>` | Add new user (root only) |
| `clear` | Clear screen |
| `help` | Show help |
| `exit` | Exit file system |

#### Filesystem Config File Format

```
# Comments start with #
user,username,uid,group1,group2,...
dir,/path/to/directory,perms,owner
file,/path/to/file.txt,perms,owner,content

# Example:
user,alice,1000,users,developers
dir,/home/alice,755,alice
file,/home/alice/readme.txt,644,alice,Welcome!
```

## 📖 Examples

### Process Scheduling Example

```bash
$ python main.py
# Select option 1 (Schedulers)
# Choose FCFS
# Load file: tests/processes_example.txt
# Option 2: Execute scheduler
# Option 3: View results
# Option 4: View metrics
```

### File System Example

```bash
$ python main.py
# Select option 2 (File System)
# Choose option 2 (Demo)

root@os-sim:/# ls
etc  home  tmp

root@os-sim:/# cd home

root@os-sim:/home# ls
alice  bob

root@os-sim:/home# cd alice

root@os-sim:/home/alice# ls -l
rw-r--r-- alice        36 readme.txt

root@os-sim:/home/alice# cat readme.txt
Welcome to Alice's home directory!

root@os-sim:/home/alice# touch myfile.txt

root@os-sim:/home/alice# echo "Hello World" > myfile.txt

root@os-sim:/home/alice# cat myfile.txt
Hello World

root@os-sim:/home/alice# chmod 600 myfile.txt

root@os-sim:/home/alice# ls -l myfile.txt
rw------- alice        12 myfile.txt

root@os-sim:/home/alice# tree /
/
├── etc/
├── home/
│   ├── alice/
│   │   ├── readme.txt
│   │   └── myfile.txt
│   └── bob/
└── tmp/
```

## 🛠️ Development

### Code Style

- **Documentation**: English docstrings
- **Typing**: Type hints for function signatures
- **Naming**: Descriptive variable and function names
- **Comments**: Minimal, only when necessary

### Architecture

**Process Scheduling**
- `ProcessManager` handles all process lifecycle operations
- `context_switch()` centralizes state transitions
- Schedulers use `ProcessManager` API

**File System**
- Abstract `Node` class for files and directories
- Permission checks at operation level
- Hierarchical tree structure with parent pointers

### Testing

Manual testing workflows:
1. Process scheduling with different algorithms
2. File system operations with different users
3. Permission enforcement
4. Edge cases (empty directories, permission denied, etc.)

## 📝 Implementation Status

### Module 1: Process Management
- ✅ Process class with PCB
- ✅ ProcessManager with context switching
- ✅ Process states (NEW, READY, RUNNING, TERMINATED)

### Module 2: Scheduling Algorithms
- ✅ FCFS (First Come First Served)
- ✅ SJF (Shortest Job First)
- ✅ Round Robin with configurable quantum
- ✅ Performance metrics calculation
- ✅ Timeline visualization

### Module 3: File System
- ✅ User management with UID and groups
- ✅ Unix-style permissions (rwx)
- ✅ Hierarchical directory structure
- ✅ File and directory operations
- ✅ 18+ Linux-like commands
- ✅ CLI interface
- ✅ Config file loader
- ✅ GUI interface

### Module 4: Memory Management
- ⏳ Not yet implemented

## 👥 Authors

- **Juan Camilo Castro Montoya** - [chunaka](https://github.com/chunaka)

## 📄 License

This project is part of an Operating Systems course.

## 🙏 Acknowledgments

- Operating Systems course materials
- Unix/Linux documentation for filesystem design
- Process scheduling algorithms from textbooks