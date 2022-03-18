'''
消息模块
'''

from Config import config
from .message import Messenger

sckey = config.Message.sckey
message = Messenger(sckey)

def sendMessage(mes):
    message.send(mes)
