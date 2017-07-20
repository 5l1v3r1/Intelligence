from  dbmanagment.dbmanagment import DbClient



from feeds.feedparent import FeederParent
import core.common as request
from constants.values import *
import datetime
import re


_name_ = "Maxmind"
__by__ = "Maxmind.com"
__info__ = "IP addresses in the minFraud network that have been identified as higher risk."
__collection__="ip"


class Maxmind(FeederParent):
    __type__ = Type.Ip
    def __init__(self, type=__type__, name=_name_,by=__by__,sourcelink=Feeders.maxmind.s_link,updateinterval=Feeders.maxmind.u_interval):
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
        date = datetime.datetime.now().date().__str__()
        for item in self.intelligence:
            intelligence = {
                '_id': item,
                "lastDate": date,
                'type': getType(self.type),
                'description': __info__,
                'by': self.by,
                'risk': 10,
                "Intelligence":
                    [{
                        "lastDate": date,
                        "datechunk": [date],
                        'type': getType(self.type),
                        'description': __info__,
                        'by': self.by,
                        'risk': 10,
                    }]

            }
            documents.append(intelligence)
        return documents

    def extract(self,content):
        for match in re.finditer(r"high-risk-ip-sample/([\d.]+)", content):
            print(match.group(1))

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



a=Maxmind()
print(a.checkstatus(a.sourcelink))
a.getIntelligent()
a.insertdb()













