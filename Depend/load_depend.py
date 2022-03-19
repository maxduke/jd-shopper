import re

try:
    from Config import config
    from Logger import logger
    loggerError = logger.error
    REQUIREMENTS = config.path + config.Depend.path + config.Depend.file
except:
    import os
    loggerError = print
    REQUIREMENTS = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/requirements.txt"


def loadDepend():
    try:
        requirements = open(REQUIREMENTS, 'r')
    except:
        err = "Turbon Depend module opened, howerver no found " + REQUIREMENTS
        loggerError(err)
        raise Exception(err)
    libs = requirements.readlines()
    libList = []
    for lib in libs:
        try:
            name = re.search("^.+(?===)", lib).group(0)
            version = re.search("(?<===).+$", lib).group(0)
            libDict = {
                "name": name,
                "version": version
            }
            libList.append(libDict)
        except:
            continue
    return libList
