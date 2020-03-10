class TaskState:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0

class SimpleState:
    def __init__(self):
        self.task_a = TaskState()
        self.task_b = TaskState()
