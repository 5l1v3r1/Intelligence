from  dbmanagment.dbmanagment import DbClient
from feeds.feedparent import FeederParent
import core.common as request
from constants.values import *
from dateutil import parser


_name_ = "Cybersweat"
__by__ = "cybersweat.shop"
__info__ = "Performing TCP SYN to HONEYNET to a non-listening service or daemon"
__collection__="ip"


class Cybersweat(FeederParent):
    __type__ = Type.Ip
    def __init__(self, type=__type__, name=_name_,by=__by__,sourcelink=Feeders.cybersweat.s_link,updateinterval=Feeders.cybersweat.u_interval):
        FeederParent.__init__(self,type,name,by)
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.info=__info__
        self.updateinterval=updateinterval
        self.log=getlog()                           #this comming from constans

    def checkstatus(self,url=Feeders.maxmind.s_link):
        return request.checkstatus(url)  #link is available

    def getIntelligent(self):
        content=request.getPage(self.sourcelink)
        if content!=False:
            self.extract(content)

    def createDocuments(self):
        documents = []
        for item in self.intelligence:
            date=parser.parse(item[1])
            intelligence = {
                '_id': item[0],
                "lastDate": date,
                'type': getType(self.type),
                'description': __info__,
                'by': self.by,
                'risk': 9,
                "Intelligence":
                    [{
                        "lastDate": date,
                        "datechunk": [date],
                        'type': getType(self.type),
                        'description': __info__,
                        'hitscount': item[2],
                        'by': self.by,
                        'risk': 9,
                    }]

            }
            documents.append(intelligence)
        return documents

    def extract(self,content):
        for line in content:
            if line.startswith('#') or not line:
                pass
            else:
                data=line.split(';')
                self.intelligence.append([data[0],data[1],data[3].split(':')[1].strip()])  #ip ,date

    def insertdb(self):
        if len(self.intelligence)>1:
            client = DbClient()
            client.set_database('intelligence')
            client.set_collection(__collection__)
            client.insert_many(self.createDocuments())
        else:
            self.log.info("Intelligece empty")

    def __str__(self):
        return "%s  %s  %s " % (self.name, self.type, self.by)


a=Cybersweat()
a.checkstatus(a.sourcelink)
a.getIntelligent()
a.insertdb()













