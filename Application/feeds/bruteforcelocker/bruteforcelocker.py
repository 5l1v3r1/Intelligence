from  dbmanagment.dbmanagment import DbClient
import re

import core.common as request
from feeds.feeder import Feeder
from constants.values import *



__url__ = "http://danger.rulez.sk/projects/bruteforceblocker/blist.php"
__name__ = "BruteForceBlocker"
__by__ = "BruteForceBlocker"
__info__ = "Its main purpose is to block SSH bruteforce attacks via firewall.count show number of atttemps "
__collection__="ip"
__reference__ = "rulez.sk"
class bruteforcelocker(Feeder):
    __type__ = Type.Ip
    def __init__(self, type=__type__, name=__name__,by=__by__,sourcelink=Const.bruteforclocker.s_link,updateinterval=30):
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
        #([a[0]], a[2][1:], a[4])  # ip,date,count
        documents = []

        for item in self.intelligence:
            intelligence = {
                '_id': item[0],
                "lastDate": item[1],
                'type':getType(self.type),
                'description': __info__,
                'by': self.by,
                'risk': "No info",
                "Intelligence":
                    [{
                          "count":item[2],
                          "lastDate": item[1],
                          'type':getType(self.type),
                          'description': __info__,
                          'by': self.by,
                         'risk': "No info",
                    }]

            }
            documents.append(intelligence)
        return documents

    def extract(self,content):



        for line in content:

            if not line or line.startswith('#'):
               continue
            else:
                a=line.split('\t')
                self.intelligence.append([a[0],a[2][1:],a[4]]) #ip,date,count

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













