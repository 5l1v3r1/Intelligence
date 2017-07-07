from  dbmanagment.dbmanagment import DbClient
import re

import core.common as request
from feeds.feeder import Feeder
from constants.values import *



__url__ = "http://danger.rulez.sk/projects/bruteforceblocker/blist.php"
__name__ = "BruteForceBlocker"
__by__ = "BruteForceBlocker"
__info__ = "Its main purpose is to block SSH bruteforce attacks via firewall."
__collection__="ip"
__reference__ = "rulez.sk"
class bruteforcelocker(Feeder):
    __type__ = Type.Ip
    def __init__(self, type=__type__, name=__name__,by=__by__,sourcelink=Const.bru.s_ip_link,updateinterval=12*60):
        Feeder.__init__(self,type,name,by)
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.updateinterval=updateinterval
        self.log=getlog()                           #this comming from constans

    def checkstatus(self,url):
        return request.checkstatus(url)  #link is available

    def getIntelligent(self):
        content=request.getPage(self.sourcelink)
        if content!=False:
            self.extract(content)

    def createDocuments(self):
        documents = []
        date=self.intelligence[0]['date']
        categorty=self.intelligence[0]['category']
        for item in self.intelligence[1:]:
            intelligence = {
                '_id': item,
                "lastDate": date,
                'type':categorty,
                'description': __info__,
                'by': self.by,
                'risk': "No info",
                "Intelligence":
                    [{
                         'type':categorty,
                         'description': __info__,
                         'by': self.by,
                         'risk': "No info"
                    }]

            }
            documents.append(intelligence)
        return documents

    def extract(self,content):



        for line in content:

            if not line or line.startswith('#'):
                if line.startswith('# This File Date'):
                    date = line.split(':')[1]
                    self.intelligence[0]["date"] = date
                    continue
                elif line.startswith('# Category'):
                    self.intelligence[0]["category"] = line.split(':')[1]
                    continue
            else:
                self.intelligence.append(line)

    def insertdb(self):
        if len(self.intelligence)>1:
            client = DbClient()
            client.setdatabase('intelligence')
            client.setcollection(__collection__)
            client.insertmany(self.createDocuments())
        else:
            self.log.info("Intelligece empty")

    def __str__(self):
        return "%s  %s  %s " % (self.name, self.type, self.by)



a=bruteforcelocker()
print(a.checkstatus(a.sourcelink))
a.getIntelligent()
a.insertdb()













