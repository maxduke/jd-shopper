import time
import datetime


class Progress(object):
    startTime = time.time()
    left_sign = '█'
    # left_sign = '░'
    # right_sign = '-'
    right_sign = ' '
    lens = 20
    delay = 0.05

    def __init__(self, total, name='Progress'):
        self.count = 0
        self.total = total
        self.name = name
        self.multiple = self.lens / self.total
        self.progress = 0
        self.percent = 0

    def update(self):
        self.count += 1
        self.progress = int(self.count * self.multiple)
        self.percent = self.progress * int(100 / self.lens)
        percentChar = str(self.percent) + "%"
        doneSign = self.progress * self.left_sign
        dontSign = (self.lens - self.progress) * self.right_sign
        leftTime = self.getLeftTime()
        print("\r{}: {:<4} |{}{}| [{}/{}]({})".format(
            self.name, percentChar, doneSign, dontSign, self.count, self.total, leftTime), end="", flush=True)

    def done(self):
        print("\r{}: {:<4} |{}{}| [{}/{}]({})".format(
            self.name, '100%', self.lens * self.left_sign, '', self.count, self.total, '00:00:00'), flush=True)

    def getNowTime(self):
        return int(time.time() - self.startTime)

    def getLeftTime(self):
        nowTime = self.getNowTime()
        leftTimeSecs = int(nowTime / (self.percent / 100)) - nowTime if self.percent > 0 else 0
        leftTime = str(datetime.timedelta(seconds=leftTimeSecs))
        leftTime = leftTime if len(leftTime) > 7 else '0' + leftTime
        return leftTime if leftTimeSecs > 0 else '00:00:00'


def progress(num):
    p = Progress(num, "Start")
    for i in range(num):
        p.update()
        time.sleep(0.5)
    p.done()
