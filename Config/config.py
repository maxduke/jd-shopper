import yaml
import os
from Config.direct import Direct

CONFIG = {
    'ROOT_PATH': os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'CONFIG_PATH': '/Config/',
    'CONFIG_FILE': 'config.yaml'
}


class Config(object):

    def __init__(self):
        self.file = CONFIG['ROOT_PATH'] + CONFIG['CONFIG_PATH'] + CONFIG['CONFIG_FILE']
        self.data = self.read()
        self.direct = Direct(self.data)
        self.direct.path = CONFIG['ROOT_PATH']
        self.direct.raw = self.data

    def read(self):
        # 打开yaml文件
        file = open(self.file, 'r', encoding="utf-8")
        file_data = file.read()
        file.close()
        # 将字符串转化为字典或列表
        return yaml.full_load(file_data)
