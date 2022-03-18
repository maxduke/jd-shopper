from Core import core
from Logger import logger
from Scheduler import Scheduler
from Config import config
from Server import server
from threading import Thread
from GUI.gui import gui
from concurrent.futures import ProcessPoolExecutor

PROCESS_MODE = config.Server.process_mode
SCHEDULER = config.Scheduler.open
SERVER = config.Server.open
GUI = config.GUI.open


def running():
    if not SCHEDULER:
        thread_core = Thread(target=core)
        thread_core.start()
    else:  # 调度器开启后core函数将被scheduler调度器代理，开启定时执行core
        startTime = config.Scheduler.time
        skipWeekend = config.Scheduler.skip_weekend
        scheduler = Scheduler(task=core, startTime=startTime, skipWeekend=skipWeekend)
    if SERVER:
        if PROCESS_MODE:
            work_count = config.Server.process_count
            server_process(work_count)
        else:
            thread_server = Thread(target=server)
            thread_server.start()
    if GUI:
        gui()


def server_process(work_count=4):
    with ProcessPoolExecutor(work_count) as pool:
        for i in range(work_count):
            pool.submit(server())


if __name__ == "__main__":
    DEBUG = config.Debug.open
    if DEBUG:
        logger.info("\n===== DEBUG MODE =====")
        core()
    else:
        running()
