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
    

    def update_state(self, new_state:ProcessState, current_time:int=0) -> None:
        """
        Update process state
        """
        self.state = new_state
        if new_state == ProcessState.RUNNING and self.start_time == -1 and current_time != 0:
            self.start_time = current_time
    
    
    def increment_cpu_time(self, time_units:int) -> None:
        """ 
        Simulate CPU usage
        """

        self.remaining_time = max(0, self.remaining_time - time_units)
        self.program_counter += time_units

    def is_completed(self) -> bool:
        """
        Check if process has finished
        """
        return self.remaining_time <= 0 

    def calculate_metrics(self, current_time:int) -> None:
        """
        Calculate waiting and turnaround times
        """
        if self.state == ProcessState.TERMINATED:
            self.completion_time = current_time
            self.turnaround_time = self.completion_time - self.arrival_time
            self.waiting_time = self.turnaround_time - self.burst_time
            
            if self.response_time == -1 and self.start_time != -1:
                self.response_time = self.start_time - self.arrival_time
    
    def __str__(self):
        return (f"PCB(PID={self.pid}, State={self.state.value}, Remaining={self.remaining_time}, Priority={self.priority})")