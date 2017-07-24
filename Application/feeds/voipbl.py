import datetime
from  dbmanagment.dbmanagment import DbClient
from feeds.feedparent import FeederParent
import core.common as request
from core.addroperation import get_iplist
from constants.values import *
from dateutil import parser



_name_ = "VoIP"
__by__ = "voipbl.org"
__info__ = "VoIP blacklist that is aimed to protects against VoIP Fraud "
__collection__="ip"

class Voipbl(FeederParent):
    __type__ = Type.Ip
    def __init__(self, type=__type__, name=_name_,by=__by__,sourcelink=Feeders.voipbl.s_link,updateinterval=Feeders.voipbl.u_interval):
        FeederParent.__init__(self, type, name,by)
        self.intelligence = []
        self.sourcelink = sourcelink
        self.info = __info__
        self.updateinterval = updateinterval
        self.log = getlog()                           #this comming from constans

    def checkstatus(self,url=Feeders.voipbl.s_link):
        return request.checkstatus(url)  #link is available

    def getIntelligent(self):
        content=request.getPage(self.sourcelink)
        if content!=False:
            self.extract(content)

    def createDocuments(self):
        uniqelist = set(self.intelligence)  #todo belki tekrara edenler için farkli bişey yapilabilir
        documents = []
        date = parser.parse(datetime.datetime.now().date().__str__())
        for item in uniqelist:
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
            if line.startswith('#') or not line:
                pass
            else:
                ip=get_iplist(line.strip('\n'))
                if type(ip) == type([]):
                    for i in ip:
                        self.intelligence.append(i)
                else:
                    self.intelligence.append(ip)


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

#a=Voipbl()
#print(a.checkstatus())
#a.getIntelligent()
#a.insertdb()


