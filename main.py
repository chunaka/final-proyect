from ui.console import ConsoleUI
from schedulers.fcfs import FCFSScheduler
from schedulers.sjf import SJFScheduler

def main():
    # Mostrar menú de selección de scheduler
    print("=" * 50)
    print("SIMULADOR DE PLANIFICACIÓN DE PROCESOS")
    print("=" * 50)
    print("\nSeleccione el algoritmo de planificación:")
    print("1. FCFS (First Come First Served)")
    print("2. SJF (Shortest Job First)")
    print("=" * 50)
    
    schedulers = {
        "1": FCFSScheduler,
        "2": SJFScheduler
    }
    
    # Solicitar selección del usuario
    while True:
        choice = input("\nIngrese su opción (1-2): ").strip()
        if choice in schedulers:
            selected_scheduler = schedulers[choice]
            scheduler_name = "FCFS" if choice == "1" else "SJF"
            print(f"\n[OK] Scheduler seleccionado: {scheduler_name}\n")
            break
        else:
            print(f"[ERROR] Opción inválida: {choice}")
    
    ui = ConsoleUI(selected_scheduler)

    while True:
        option = ui.show_menu()
        
        if option == "1":
            path = input("Ruta del archivo: ")
            ui.load_processes(path)

        elif option == "2":
            ui.run_scheduler()
            
        elif option == "3":
            ui.show_results()

        elif option == "4":
            ui.show_metrics()

        elif option == "5":
            print("Saliendo...")
            break

        else:
            print(f"[ERROR] Opción inválida: {option}")

if __name__ == "__main__":
    main()