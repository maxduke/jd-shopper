import re
from Config import config
from Logger import logger

REQUIREMENTS = config.path + config.Depend.path + config.Depend.file


def loadDepend():
    try:
        requirements = open(REQUIREMENTS, 'r')
    except:
        err = "Turbon Depend module opened, howerver no found " + REQUIREMENTS
        logger.error(err)
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
