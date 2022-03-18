from Depend.load_depend import loadDepend
from Logger import logger


def importLib():
    """Load python dependent libraries dynamically"""
    logger.info('Load dependent libraries dynamically')

    libList = loadDepend()

    from pip._internal import main as pip_main
    import importlib

    def install(package):
        pip_main(['install', package])

    createVar = locals()

    for lib in libList:
        logger.info(f"{lib['name']} - {lib['version']}")
        try:
            createVar[lib["name"]] = importlib.import_module(lib["name"])
        except Exception as e:
            try:
                install(f'{lib["name"]}=={lib["version"]}')
                createVar[lib["name"]] = importlib.import_module(lib["name"])
            except Exception as e:
                logger.error(e)

    logger.info('Load libraries complete')
