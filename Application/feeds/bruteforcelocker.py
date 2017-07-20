from  dbmanagment.dbmanagment import DbClient
from feeds.feedparent import FeederParent
import core.common as core
from constants.values import *


_name_ = "BruteForceBlocker"
__by__ = "BruteForceBlocker"
__info__ = "Its main purpose is to block SSH bruteforce attacks via firewall.count show number of atttemps "
__collection__="ip"
__reference__ = "rulez.sk"
maxcount = 0
class Bruteforcelocker(FeederParent):
    __type__ = Type.Ip
    def __init__(self, type=__type__, name=_name_,by=__by__,sourcelink=Feeders.bruteforclocker.s_link,updateinterval=30):
        FeederParent.__init__(self,type,name,by)
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.updateinterval=updateinterval
        self.log=getlog()                           #this comming from constans

    def checkstatus(self,url=Feeders.bruteforclocker.s_link):
        return core.checkstatus(url)  #link is available

    def getIntelligent(self):
        content=core.getPage(self.sourcelink)
        if content!=False:
            self.extract(content)

    def createDocuments(self):
        #([a[0]], a[2][1:], a[4])  # ip,date,count
        documents = []

        for item in self.intelligence:
            date = core.parser.parse(item[1])
            intelligence = {
                '_id': item[0],
                "lastDate": date,
                'type':getType(self.type),
                'description': __info__,
                'by': self.by,
                'risk': self.get_risk(int(item[2])),
                "Intelligence":
                    [{
                          "lastDate": date,
                          "datechunk": [date],
                           "count": item[2],
                          'type':getType(self.type),
                          'description': __info__,
                          'by': self.by,
                          'risk': self.get_risk(int(item[2])),
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
            client.set_database('intelligence')
            client.set_collection(__collection__)
            client.insert_many(self.createDocuments())
        else:
            self.log.info("Intelligece empty")


    def get_risk(self,count):
        global maxcount
        if maxcount <= count:
            maxcount = count
        risk = (int(count*(10/maxcount))+3)
        if risk>10:
            return 10
        return risk

    def __str__(self):
        return "%s  %s  %s " % (self.name, self.type, self.by)


#a=Bruteforcelocker()
#print(a.checkstatus(a.sourcelink))
#a.getIntelligent()
#a.insertdb()










