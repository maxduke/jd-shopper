from Depend.load_depend import loadDepend

try:
    from Logger import logger
    loggerInfo = logger.info
    loggerError = logger.error
except:
    loggerInfo = print
    loggerError = print


def importLib(alias=None):
    """Load python dependent libraries dynamically"""
    loggerInfo('Load dependent libraries dynamically')

    libList = loadDepend()

    from pip._internal import main as pip_main
    import importlib

    def install(package):
        pip_main(['install', package])

    createVar = locals()

    for lib in libList:
        libName = lib['name']
        version = lib['version']
        if libName in alias:
            moduleName = alias[libName]
        else:
            moduleName = libName
        loggerInfo(f'{libName} - {version}')
        try:
            createVar[moduleName] = importlib.import_module(moduleName)
        except Exception as e:
            try:
                install(f'{libName}=={version}')
                createVar[moduleName] = importlib.import_module(moduleName)
            except Exception as e:
                loggerError(e)

    loggerInfo('Load libraries complete')
