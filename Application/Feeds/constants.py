from enum import Enum
import logging

class Type(Enum):
    Ip=1
    Domain=2
    Mail=3
    Malware=4

class Const:
    class autoshun:
        s_link = 'https://www.autoshun.org/download/?api_key=d4066260862da9118d84717e17c0fc&format=csv'
        u_interval=10 #minute interval
    class dbmanagment:
        db_path = 'mongodb://arquanum:qPuDqX2e@138.68.92.9:27017/admin'





def getlog():
    logFormatter = logging.Formatter(
        "%(asctime)s [%(filename)s  %(funcName)s %(lineno)s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()

    if (len(rootLogger.handlers) > 0):
        return rootLogger
    rootLogger.setLevel(logging.INFO)
    fileHandler = logging.FileHandler('logfile.log')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    return rootLogger