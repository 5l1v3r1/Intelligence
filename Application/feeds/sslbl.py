from  dbmanagment.dbmanagment import DbClient



from feeds.feedparent import FeederParent
import core.common as request
from constants.values import *
from dateutil import parser



_name_ = "SSL Blacklist"
__by__ = "sslbl"
__info__ = "The goal is to provide a list of 'bad' SSL certificates identified by abuse.ch to be associated with malware or botnet activities."
__collection__="ip"
__reference__ = "abuse.ch"

class Sslbl(FeederParent):
    __type__ = Type.Ip
    def __init__(self, type=__type__, name=_name_,by=__by__,sourcelink=Feeders.sslbl.s_link,updateinterval=Feeders.sslbl.u_interval):
        FeederParent.__init__(self,type,name,by)
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.info=__info__
        self.updateinterval=updateinterval
        self.log=getlog()                           #this comming from constans

    def checkstatus(self,url=Feeders.bruteforclocker.s_link):
        return request.checkstatus(url)  #link is available

    def getIntelligent(self):
        content=request.getPage(self.sourcelink)
        if content!=False:
            self.extract(content)

    def createDocuments(self):
        # DstIP,DstPort,count
        documents = []
        date=self.intelligence[0][:-5]
        date=parser.parse(date)
        for item in self.intelligence[1:]:
            intelligence = {
                '_id': item[0],
                "lastDate": date,
                'type':getType(self.type),
                'scope': item[2].strip('\n'),
                'description': __info__,
                'by': self.by,
                'risk': 8,
                "Intelligence":
                    [{
                         "lastDate": date,
                          "port":item[1],
                            'scope': item[2].strip('\n'),
                          'type':getType(self.type),
                          'description': __info__,
                          'by': self.by,
                         'risk': 8,
                    }]

            }
            documents.append(intelligence)
        return documents

    def extract(self,content):
        for line in content:

            if line.startswith('#') or not line:
                if line.startswith('# Last'):
                    date=line.split('updated:')[1][:-2]
                    date=date.strip()
                    self.intelligence.append(date)
            else:
                a=line.split(',')
                self.intelligence.append([a[0],a[1],a[2]]) #DstIP,DstPort,count

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



#a=Sslbl()
#print(a.checkstatus(a.sourcelink))
#a.getIntelligent()
#a.insertdb()













