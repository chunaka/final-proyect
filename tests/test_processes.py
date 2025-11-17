from models.pcb import PCB, ProcessState

# === CASO 1: Proceso básica ===

procesos_test1 = [
    {"pid": 1, "llegada": 0, "rafaga": 5, "usuario":"usuario1"},
    {"pid": 2, "llegada": 1, "rafaga": 3, "usuario":"usuario3"},
]

def test_creation():
    """
    """

    procesos = []

    for p in procesos_test1:
        pcb = PCB(
            pid = p["pid"],
            burst_time = p["rafaga"],
            arrival_time = p["llegada"]
        )
        procesos.append(pcb)


        for pcb in procesos:
            print(pcb)
            assert pcb.state == ProcessState.NEW
            assert pcb.remaining_time == pcb.burst_time
            assert pcb.waiting_time == 0

if __name__ == "__main__":
    test_creation()
    print("Prueba completada")