from schedulers.scheduler_base import Scheduler
from models.pcb import ProcessState

class FCFSScheduler(Scheduler):
    """
    First Come First Served
    Runs processes in the order of arrival with no preemption.
    Uses ProcessManager and context_switch for process management.
    """

    def run(self):
        """
        Execute FCFS on the list of processes using ProcessManager
        """
        # Get all processes from ready_queue and sort by arrival time
        processes = list(self.pm.ready_queue)
        processes.sort(key=lambda p: p.pcb.arrival_time)
        
        # Clear ready_queue and repopulate in sorted order
        self.pm.ready_queue.clear()
        for process in processes:
            self.pm.ready_queue.append(process)

        current_time = 0
        
        while self.pm.has_ready_processes() or self.pm.current_process:
            # If no current process, do context switch
            if not self.pm.current_process:
                # Handle idle time - jump to next process arrival
                if self.pm.has_ready_processes():
                    next_process = list(self.pm.ready_queue)[0]
                    current_time = max(current_time, next_process.pcb.arrival_time)
                    self.pm.context_switch()
                else:
                    break
            
            if self.pm.current_process:
                process = self.pm.current_process
                start = current_time
                burst = process.pcb.remaining_time
                end = start + burst
                
                # Record timeline
                self.timeline.append((process.pcb.pid, start, end))
                
                # Set start time if first execution
                if process.pcb.start_time == -1:
                    process.pcb.start_time = start
                
                # Execute process to completion
                self.pm.execute_current(burst)
                current_time = end
                
                # Set completion time and terminate
                process.pcb.completion_time = end
                self.pm.terminate_current_process(current_time)
    
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

        waiting = sum(p.pcb.start_time - p.pcb.arrival_time for p in processes) / n
        turnaround = sum(p.pcb.completion_time - p.pcb.arrival_time for p in processes) / n

        total_time = max(p.pcb.completion_time for p in processes)
        throughput = n / total_time if total_time > 0 else 0

        return {
            "avg_waiting": waiting,
            "avg_turnaround": turnaround,
            "throughput": throughput
        }