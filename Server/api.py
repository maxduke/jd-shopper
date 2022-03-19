import copy
import os
import signal
from Config import config
from Core.spider import Waiter
from threading import Thread

from Logger import logger


class Global(object):

    def __init__(self):
        self.waiter = None
        self.login = None
        self.thread = None
        self.running = False

    def update(self):
        self.login = self.waiter.qrlogin.is_login

    def stop(self):
        self.waiter.stopTag = True
        self.running = False


glo = Global()


def log(request):
    file_path = config.path + config.Logger.file_path + \
        config.Logger.file_name
    file_page_file = open(file_path, 'r', encoding="utf-8")
    return str(file_page_file.read())


def serverConfig(request):
    appConfig = copy.deepcopy(config._config._sections)
    for model in appConfig:
        for item in appConfig[model]:
            appConfig[model][item] = eval(appConfig[model][item])
            value = appConfig[model][item]
            # DEBUG print(model, item, value, type(value))
    return appConfig


def jdShopper(request):
    mode = request['mode']
    date = request['date']
    skuids = request['skuid']
    area = request['area']
    eid = request['eid']
    fp = request['fp']
    count = request['count']
    retry = request['retry']
    work_count = request['work_count']
    timeout = request['timeout']
    if mode == '1':
        glo.waiter = Waiter(skuids=skuids, area=area, eid=eid, fp=fp, count=count,
                            retry=retry, work_count=work_count, timeout=timeout)
        glo.thread = Thread(target=glo.waiter.waitForSell)
        glo.thread.start()
    elif mode == '2':
        date = date.replace("T", " ")
        date = date.replace("Z", "")
        glo.waiter = Waiter(skuids=skuids, area=area, eid=eid, fp=fp, count=count,
                            retry=retry, work_count=work_count, timeout=timeout, date=date)
        glo.thread = Thread(target=glo.waiter.waitTimeForSell)
        glo.thread.start()
    glo.update()
    if glo.login:
        glo.running = True
    return glo.login


def loginStatus(request):
    try:
        glo.update()
    except:
        pass
    if glo.login:
        glo.running = True
    return glo.login


def runningStatus(request):
    return glo.running

def stopRunning(request):
    try:
        glo.stop()
        return True
    except:
        return False

def exitProcess(request):
    logger.info('结束进程')
    os.kill(os.getpid(), signal.SIGTERM)