from enum import Enum

class ProcessState(Enum):
    """
    Enumeration of possible process states
    """

    NEW = "new"
    READY = "ready"
    RUNNING = "running"
    BLOCKED = "blocked"
    TERMINATED = "terminated"

class PCB:
    """
    Process Control Block module
    Contain all the information about a process that the OS needs to manage it.
    """
    def __init__(self, pid:int, burst_time:int, arrival_time:int=0, priority:int=0):
        """
        Initialize a new PCB
        
        Args:
            pid: Process ID (unique identifier)
            burst_time: Total CPU needed by the process
            arrival_time: Time when process arrives in the system
            priority: Process priority (lower number = higher priority)
        """
        #Basic identification
        self.pid = pid
        self.state = ProcessState.NEW
        self.program_counter = 0

        #CPU and timing info
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.arrival_time = arrival_time
        self.priority = priority

        #Scheduling metrics
        self.waiting_time = 0
        self.turnaround_time = 0
        self.response_time = -1
        self.completion_time = 0
        self.start_time = -1
        
    # def __str__(self):
    #     return (f"PCB(PID={self.pid}, User = {self.user}, State={self.state.value}, Remaining={self.remaining_time}, Priority={self.priority})")