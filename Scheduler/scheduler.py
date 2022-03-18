from Scheduler.task import Task
from threading import Thread

class Scheduler(object):

    def __init__(self, task, startTime, skipWeekend):
        """初始化"""
        self.task = task
        self.start_time = startTime
        self.skip_weekend = skipWeekend
        self.task_list = []
        self.plan()

    def plan(self):
        for timing in self.start_time:

            task = Task(self.task, timing, self.skip_weekend)
            mission = {
                'task': task,
                'thread': Thread(target=task.schedule)
            }
            mission['thread'].start()
