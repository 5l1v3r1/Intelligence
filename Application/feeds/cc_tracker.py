from  dbmanagment.dbmanagment import DbClient
from constants.values import *
from feeds.feedparent import FeederParent
import core.common as request
import csv

_name_ = "cc_tracker"
__by__ = "C&C Tracker"
__info__ = "blacklist ip feeder"
__collection__="ip"

class Cc_tracker(FeederParent):
    __type__ = Type.Ip

    def __init__(self, type=__type__, name=_name_,by=__by__,sourcelink=Feeders.cc_tracker.s_link,updateinterval=Feeders.cc_tracker.u_interval):
        FeederParent.__init__(self,type,name,by)
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.updateinterval=updateinterval
        self.log=getlog()

    def checkstatus(self,url=Feeders.cc_tracker.s_link):
        return request.checkstatus(url)  #link is available

    def getIntelligent(self):
        content=request.getPage(self.sourcelink)
        if content!=False:
            self.extract(content)


    def createDocuments(self):
        documents = []
        for item in self.intelligence[1:]:
            intelligence = {
                '_id': item[0],
                "lastDate": item[2],
                'type':item[1],
                'description': __info__,
                'source': item[3],
                'by': self.by,
                'risk': "No info",
                "Intelligence":
                    [{
                         "lastDate": item[2],
                         "datachunk":item[3:],
                         'type':item[1],
                         'description': __info__,
                        'source': item[3],
                         'by': self.by,
                          'risk': "No info",
                    }]

            }
            documents.append(intelligence)
        return documents

    def extract(self,data):
        readCSV = csv.reader(data)
        for item in readCSV:
            if item[0][0] == "#":
                pass
            else:
                self.intelligence.append(item)


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


#a=Cc_tracker()
#print(a.checkstatus(a.sourcelink))
#a.getIntelligent()
#a.insertdb()