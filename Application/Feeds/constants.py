from enum import Enum
import logging
import os
class Type(Enum):
    Ip=1
    Domain=2
    Mail=3
    Malware=4
    Phisingurl=5


def getType(type):
    if Type.Ip==type:
        return "Black_Ip"
    elif Type.Domain==type:
        return "Black_Domain"
    elif Type.Mail == type:
        return "Mail"
    elif Type.Malware == type:
        return "Malware"
    elif Type.Phisingurl == type:
        return "Phisingurl"
    else:
        return "Type not defined"

class Const:
    class autoshun:
        s_link = 'https://www.autoshun.org/download/?api_key=eb4c31917acb6afb8838ceab70a8309&format=csv'
        u_interval=30 #minute interval

    class phistank:
        s_link= 'http://data.phishtank.com/data/online-valid.csv'
        app_key='9c6f6c909a9df44bae577bcdf35d97ff87a4d07ef4243db534c8775be81cdc31'
        api_link='http://checkurl.phishtank.com/checkurl/'
        u_interval = 90 #minute interval

    class dbmanagment:
        db_path = 'mongodb://arquanum:qPuDqX2e@138.68.92.9:27017/admin'



def getlog():
    logFormatter = logging.Formatter(
        "%(asctime)s [%(filename)s  %(funcName)s %(lineno)s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()

    if (len(rootLogger.handlers) > 0):
        return rootLogger
    rootLogger.setLevel(logging.INFO)
    fileHandler = logging.FileHandler(os.getcwd()+'/logfile.log')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    return rootLogger