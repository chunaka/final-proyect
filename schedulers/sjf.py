from schedulers.scheduler_base import Scheduler
from models.pcb import ProcessState

class SJFScheduler(Scheduler):
    """
    Shortest Job First (Non-preemptive)
    Runs processes in order of shortest burst time.
    Uses ProcessManager and context_switch for process management.
    """

    def run(self):
        """
        Execute SJF on the list of processes using ProcessManager
        """
        current_time = 0
        
        while self.pm.has_ready_processes() or self.pm.current_process:
            # If no current process, do context switch to shortest job
            if not self.pm.current_process:
                if not self.pm.has_ready_processes():
                    break
                
                # Find processes that have arrived
                available = [p for p in self.pm.ready_queue if p.pcb.arrival_time <= current_time]
                
                # If no process has arrived yet, jump to next arrival time
                if not available:
                    current_time = min(p.pcb.arrival_time for p in self.pm.ready_queue)
                    available = [p for p in self.pm.ready_queue if p.pcb.arrival_time <= current_time]
                
                # Sort by burst time (shortest first) and select the shortest
                available.sort(key=lambda p: p.pcb.burst_time)
                shortest = available[0]
                
                # Move shortest to front of ready_queue
                self.pm.ready_queue.remove(shortest)
                self.pm.ready_queue.appendleft(shortest)
                
                # Context switch to shortest job
                self.pm.context_switch()
            
            if self.pm.current_process:
                process = self.pm.current_process
                start = max(current_time, process.pcb.arrival_time)
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
