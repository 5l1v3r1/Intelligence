
from  dbmanagment.dbmanagment import DbClient
from feeds.feedparent import FeederParent
import core.common as request
from constants.values import *
from dateutil import parser



_name_ = "Vx_fault"
__by__ = "vxvault.net"
__info__ = "Malware url"
__collection__="url"

class Vx_fault(FeederParent):
    __type__ = Type.Ip
    def __init__(self, type=__type__, name=_name_,by=__by__,sourcelink=Feeders.vxvault.s_link,updateinterval=Feeders.vxvault.u_interval):
        FeederParent.__init__(self, type, name,by)
        self.intelligence = []
        self.sourcelink = sourcelink
        self.info = __info__
        self.updateinterval = updateinterval
        self.log = getlog()                           #this comming from constans

    def checkstatus(self,url=Feeders.vxvault.s_link):
        return request.checkstatus(url)  #link is available

    def getIntelligent(self):
        content=request.getPage(self.sourcelink)
        if content!=False:
            self.extract(content)

    def createDocuments(self):
        documents = []
        date = self.intelligence[0]
        for item in self.intelligence[1:]:
            intelligence = {
                '_id': item,
                "lastDate": date,
                'type':getType(self.type),
                'description': __info__,
                'by': self.by,
                'risk': 9,
                "Intelligence":
                    [{
                          "lastDate": date,
                          "datechunk": [date],
                          'type':getType(self.type),
                          'description': __info__,
                          'by': self.by,
                          'risk': 9,
                    }]
            }
            documents.append(intelligence)
        return documents

    def extract(self,content):

        for line in content:
            if not line.startswith('http') or not line:
                try:
                    temp=parser.parse(line)
                    self.intelligence.append(temp)
                except ValueError:
                    pass

            else:
                self.intelligence.append(line.strip('\r\n'))


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

a=Vx_fault()
print(a.checkstatus())
a.getIntelligent()
a.insertdb()


