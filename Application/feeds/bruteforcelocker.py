from  dbmanagment.dbmanagment import DbClient



from feeds.feedparent import FeederParent
import core.common as request
from constants.values import *
from dateutil import parser



_name_ = "BruteForceBlocker"
__by__ = "BruteForceBlocker"
__info__ = "Its main purpose is to block SSH bruteforce attacks via firewall.count show number of atttemps "
__collection__="ip"
__reference__ = "rulez.sk"

class Bruteforcelocker(FeederParent):
    __type__ = Type.Ip
    def __init__(self, type=__type__, name=_name_,by=__by__,sourcelink=Feeders.bruteforclocker.s_link,updateinterval=30):
        FeederParent.__init__(self,type,name,by)
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.updateinterval=updateinterval
        self.log=getlog()                           #this comming from constans

    def checkstatus(self,url=Feeders.bruteforclocker.s_link):
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
                "lastDate": parser.parse(item[1]),
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



#a=Bruteforcelocker()
#print(a.checkstatus(a.sourcelink))
#a.getIntelligent()
#a.insertdb()













