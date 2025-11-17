from ui.console import ConsoleUI
from schedulers.fcfs import FCFSScheduler

def main():
    ui = ConsoleUI(FCFSScheduler)

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