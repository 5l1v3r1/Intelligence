from  dbmanagment.dbmanagment import DbClient
from constants.values import *
from feeds.feedparent import FeederParent
import core.common as request


_name_ = "packetmail"
__by__ = "Packetmail"
__info__ = "blacklist ip feeder"
__collection__="ip"
__type__ = Type.Ip

class Packetmail(FeederParent):

    def __init__(self, type=__type__, name=_name_,by=__by__,sourcelink=Feeders.packetmail.s_link,updateinterval=Feeders.packetmail.u_interval):
        FeederParent.__init__(self,type,name,by)
        self.intelligence = []
        self.sourcelink = sourcelink
        self.updateinterval = updateinterval
        self.log = getlog()

    def checkstatus(self,url=Feeders.packetmail.s_link):
        return request.checkstatus(url)  #link is available

    def getIntelligent(self):
        content=request.getPage(self.sourcelink)
        if content!=False:
            self.extract(content)


    def createDocuments(self):
        documents = []

        for item in self.intelligence[1:]:
            intelligence = {
                '_id': item.split()[7],
                "lastDate": item.split()[5],
                'type':getType(self.type),
                'description': __info__,
                'by': self.by,
                'risk': 3,
                "Intelligence":
                    [{
                         "lastDate": item.split()[5],
                        'type':getType(self.type),
                         'description': __info__,
                         'by': self.by,
                         'risk': 3,
                    }]

            }
            documents.append(intelligence)
        return documents

    def extract(self,data):
        for item in data:
            if item[0][0] == "#":
                pass
            else:
                self.intelligence.append(item)


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


#a=Packetmail()
#print(a.checkstatus(a.sourcelink))
#a.getIntelligent()
#a.insertdb()