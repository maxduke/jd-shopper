"""
依赖管理模块
"""
from .import_lib import importLib
from Config import config

alias = {
    'pyyaml': 'yaml',
}

DEPEND = config.Depend.open
if DEPEND:
    importLib(alias)