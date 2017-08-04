from  dbmanagment.dbmanagment import DbClient
from feeds.feedparent import FeederParent
import core.common as request
from constants.values import *
from dateutil import parser


_name_ = "https://myip.ms/files/blacklist/htaccess/latest_blacklist.txt"
__by__ = "myip.ms"
__info__ = "LIVE BLACKLIST IPv4/IPv6"
__collection__="ip"


class Myip(FeederParent):
    __type__ = Type.Ip
    def __init__(self, type=__type__, name=_name_,by=__by__,sourcelink=Feeders.myip.s_link,updateinterval=Feeders.myip.u_interval):
        FeederParent.__init__(self,type,name,by)
        self.intelligence = []
        self.sourcelink = sourcelink
        self.info = __info__
        self.updateinterval = updateinterval
        self.log = getlog()                           #this comming from constans

    def checkstatus(self,url=Feeders.maxmind.s_link):
        return request.checkstatus(url)  #link is available

    def getIntelligent(self):
        content=request.getPage(self.sourcelink)
        if content!=False:
            self.extract(content)

    def createDocuments(self):
        documents = []
        date = parser.parse(self.intelligence[0])
        for item in self.intelligence[1:]:

            intelligence = {
                '_id': item,
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
                        'by': self.by,
                        'risk': 9,
                    }]

            }
            documents.append(intelligence)
        return documents

    def extract(self,content):
        for line in content:
            if line.startswith('#') or not line or line.startswith('\n'):
                if line.startswith('# on'):
                    self.intelligence.append(line.split(',')[1].split('Last')[0].strip())
            else:
                ip=line.split('from')[1].strip()
                self.intelligence.append(ip)  #ip ,date


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


a=Myip()
a.checkstatus(a.sourcelink)
a.getIntelligent()
a.insertdb()
