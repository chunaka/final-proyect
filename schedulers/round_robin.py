from schedulers.scheduler_base import Scheduler
from models.pcb import ProcessState

class RoundRobinScheduler(Scheduler):
    """
    Round Robin (Preemptive)
    Runs processes in a circular queue with a fixed time quantum.
    Uses ProcessManager and context_switch for preemptive scheduling.
    This is the ideal use case for context_switch demonstration.
    """

    def __init__(self, process_manager, quantum=2):
        """
        Initialize Round Robin scheduler with a time quantum.
        
        Args:
            process_manager: ProcessManager instance
            quantum (int): Time quantum for each process slice (default: 2)
        """
        super().__init__(process_manager)
        self.quantum = quantum

    def run(self):
        """
        Execute Round Robin using ProcessManager's context_switch
        """
        # Sort processes by arrival time
        processes = list(self.pm.ready_queue)
        processes.sort(key=lambda p: p.pcb.arrival_time)
        
        # Clear and repopulate ready_queue in sorted order
        self.pm.ready_queue.clear()
        for process in processes:
            self.pm.ready_queue.append(process)
        
        current_time = 0
        total_processes = len(processes)
        completed = 0
        
        # Track first start time for each process
        first_start = {}
        
        while completed < total_processes:
            # If no current process, context switch to next
            if not self.pm.current_process:
                if not self.pm.has_ready_processes():
                    # No process ready, should not happen but handle gracefully
                    break
                
                # Check if we need to wait for next arrival
                next_process = list(self.pm.ready_queue)[0]
                if next_process.pcb.arrival_time > current_time:
                    current_time = next_process.pcb.arrival_time
                
                # Perform context switch
                self.pm.context_switch()
            
            if self.pm.current_process:
                process = self.pm.current_process
                
                # Record first start time
                if process.pcb.pid not in first_start:
                    first_start[process.pcb.pid] = current_time
                    process.pcb.start_time = current_time
                
                # Execute for quantum or remaining time, whichever is smaller
                execution_time = min(self.quantum, process.pcb.remaining_time)
                start = current_time
                end = start + execution_time
                
                # Record timeline
                self.timeline.append((process.pcb.pid, start, end))
                
                # Execute the process
                self.pm.execute_current(execution_time)
                current_time = end
                
                # Check if process completed
                if process.is_completed():
                    process.pcb.completion_time = current_time
                    self.pm.terminate_current_process(current_time)
                    completed += 1
                else:
                    # Process not completed - context switch will move it to back of queue
                    # This is where context_switch really shines!
                    self.pm.context_switch()
    
    def compute_metrics(self):
        """
        Compute waiting time, turnaround time and throughput
        """
        processes = self.pm.terminated_list
        n = len(processes)
        
        if n == 0:
            return {
                "avg_waiting": 0,
                "avg_turnaround": 0,
                "throughput": 0
            }

        # Waiting time = start_time - arrival_time
        waiting = sum(p.pcb.start_time - p.pcb.arrival_time for p in processes) / n
        
        # Turnaround time = completion_time - arrival_time
        turnaround = sum(p.pcb.completion_time - p.pcb.arrival_time for p in processes) / n

        total_time = max(p.pcb.completion_time for p in processes)
        throughput = n / total_time if total_time > 0 else 0

        return {
            "avg_waiting": waiting,
            "avg_turnaround": turnaround,
            "throughput": throughput
        }
