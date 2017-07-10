from enum import Enum
import logging
import os,sys
from importlib import import_module









class Type(Enum):
    Ip=1
    Domain=2
    Url=3
    Mail=4
    Malware_url=5
    Malware_ip = 6
    Malware_domain = 7
    Phisingurl=8
    Ransomware = 9



def getType(type):
    if Type.Ip==type:
        return "Black_Ip"
    elif Type.Domain==type:
        return "Black_Domain"
    elif Type.Mail == type:
        return "Mail"
    elif Type.Phisingurl == type:
        return "Phisingurl"
    elif Type.Ransomware == type:
        return "Ransomware"
    elif Type.Malware_url==type:
        return "Malware_Url_Blocklist"
    elif Type.Malware_ip == type:
        return "Malware_Ip_Blocklist"
    elif Type.Malware_domain == type:
        return "Malware_Domain_Blocklist"
    else:
        return "Type not defined"

def getCollectName(type):
      if type.value in (5,3):
          return "url"
      elif type.value in (1,6):
          return "ip"
      elif type.value in (2,7):
          return "domain"


class Feeders:
    config=import_module
    class autoshun:
        s_link   = 'https://www.autoshun.org/download/?api_key=eb4c31917acb6afb8838ceab70a8309&format=csv'
        u_interval=30        #minute interval
        def returnObject(self):
            return  import_module("feeds.autoshun").Feederautoshun()


    class malwr:
        s_link   = 'https://malwr.com'
        def returnObject(self):
            return None

    class virustotal:
        s_link   = 'https://www.virustotal.com/vtapi/v2/'
        api_key  = "51d9c4723d084b9270bda8897d8f697b005ce939d67013915af92f721e0a8634"
        def returnObject(self):
            return None

    class openphish:
        s_link   = 'https://openphish.com/feed.txt'
        u_interval = 20  # minute interval
        def returnObject(self):
            return import_module("feeds.openphish").Feederopenphish()

    class bruteforclocker:
        s_link   = 'http://danger.rulez.sk/projects/bruteforceblocker/blist.php'
        u_interval = 20  # minute interval
        def returnObject(self):
            return import_module("feeds.bruteforcelocker").bruteforcelocker()
    class ransomware:
        s_link   = 'http://ransomwaretracker.abuse.ch/blocklist/'
        u_interval = 20  # minute interval
        def returnObject(self):
            return import_module("feeds.ransomwaretracker").Feederransomwre()

    class malwaredomains_dns:
        s_link = "https://www.malwaredomainlist.com/hostslist/hosts.txt"
        u_interval = 10  # minute interval
        def returnObject(self):
            return import_module("feeds.malwaredomains_dns").md_dns()

    class malwaredomains_ip:
        u_interval = 12 * 60
        s_link = "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/malwaredomainlist.ipset"
        def returnObject(self):
            return import_module("feeds.malwaredomains_ip").md_ip()

    class malwaredomains_domain:
        u_interval = 60
        s_link = "http://malwaredomains.lehigh.edu/files/domains.txt"
        def returnObject(self):
            return import_module("feeds.malwaredomains_domains").md_domains()

    class phistank:
        s_link   = 'http://data.phishtank.com/data/online-valid.csv'
        app_key  ='9c6f6c909a9df44bae577bcdf35d97ff87a4d07ef4243db534c8775be81cdc31'
        api_link ='http://checkurl.phishtank.com/checkurl/'
        u_interval = 90 #minute interval
        def returnObject(self):
            return import_module("feeds.phishtank").Feederphistank()





def getlog():
    logFormatter = logging.Formatter(
        "%(asctime)s [%(filename)s  %(funcName)s %(lineno)s] [%(levelname)-5.5s]  %(message)s")
    rootLogger = logging.getLogger()

    if (len(rootLogger.handlers) > 0):
        return rootLogger
    rootLogger.setLevel(logging.INFO)
    fileHandler = logging.FileHandler(os.getcwd()+'/../logfile.log')
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)
    return rootLogger