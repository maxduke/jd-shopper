"""
依赖管理模块
"""

try:
    from Config import config
    DEPEND = config.Depend.open
except:
    DEPEND = True

alias = {
    'pyyaml': 'yaml',
}

if DEPEND:
    from .import_lib import importLib
    importLib(alias)