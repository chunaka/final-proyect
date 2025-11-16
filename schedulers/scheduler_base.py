class Scheduler:
    """
    Base Scheduler class.
    Provides common structures for all scheduling algorithms.
    """
    def __init__(self) -> None:
        self.processes = []
        self.timeline = []

    def add_process(self, process):
        self.processes.append(process)

    def run(self):
        """
        Must be implemented by subclasses.
        """
        raise NotImplementedError
    
    def compute_metrics(self):
        """
        Must be implemented by subclasses.
        """
        raise NotImplementedError

