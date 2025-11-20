from schedulers.scheduler_base import Scheduler

class FCFSScheduler(Scheduler):
    """
    First Come First Served
    Runs processes in the order of arrival with no preemption.
    """

    def run(self):
        """
        Execute FCFS on the list of processes
        """
        self.processes.sort(key=lambda p: p.arrival_time)

        current_time = 0
        for process in self.processes:
            start = max(current_time, process.arrival_time)
            end = start + process.burst_time

            self.timeline.append((process.pid, start, end))

            process.start_time = start
            process.completion_time = end

            current_time = end
    
    def compute_metrics(self):
        """
        Compute waiting time, turnaround time and throughput
        """
        n = len(self.processes)

        waiting = sum(process.start_time - process.arrival_time for process in self.processes) / n
        turnaround = sum(process.completion_time - process.arrival_time for process in self.processes) / n

        total_time = max(process.completion_time for process in self.processes)
        throughput = n / total_time

        return {
            "avg_waiting": waiting,
            "avg_turnaround": turnaround,
            "throughput": throughput
        }