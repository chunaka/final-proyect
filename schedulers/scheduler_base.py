class Scheduler:
    """
    Base Scheduler class.
    Provides common structures for all scheduling algorithms.
    """
    def __init__(self, process_manager) -> None:
        self.pm = process_manager
        self.timeline = []

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

