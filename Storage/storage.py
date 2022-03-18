import os
import json
from Config import config
from Logger import logger
from Storage import Reactive


class Storage(object):
    def __init__(self):
        self.data = Reactive({}, self.save)
        self.path = config.path + config.Storage.path
        self.file = self.path + config.Storage.name
        self.initialize()

    def initialize(self):
        if self.load() is None:
            self.save()

    def load(self):
        logger.info("Load Local Storage")
        if os.path.exists(self.file):
            with open(self.file, "r") as storage:
                data = json.load(storage)
                if data == "":
                    self.data = Reactive({}, self.save)
                else:
                    self.data = Reactive(data, self.save)
                return self.data
        else:
            return None

    def save(self):
        logger.info("Save Local Storage")
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        with open(self.file, "w") as storage:
            storage.seek(0)
            storage.truncate()  # clear file
            data = self.data.read().replace("'", '"')
            data = json.loads(data)
            data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'))
            storage.write(data)



