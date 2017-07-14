from  dbmanagment.dbmanagment import DbClient



from feeds.feedparent import FeederParent
import core.common as request
from constants.values import *
from dateutil import parser
import datetime

from bs4 import  BeautifulSoup


_name_ = "GreenSnow"
__by__ = "GreenSnow.co"
__info__ = "GreenSnow is comparable with SpamHaus.org for attacks of any kind except for spam. Our list is updated automatically and you can withdraw at any time your IP address if it has been listed"
__collection__="ip"


class Grensnow(FeederParent):
    __type__ = Type.Ip
    def __init__(self, type=__type__, name=_name_,by=__by__,sourcelink=Feeders.greensnow.s_link,updateinterval=Feeders.greensnow.u_interval):
        FeederParent.__init__(self,type,name,by)
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.info=__info__
        self.updateinterval=updateinterval
        self.log=getlog()                           #this comming from constans

    def checkstatus(self,url=Feeders.greensnow.s_link[0]):
        return request.checkstatus(url)  #link is available

    def getIntelligent(self):
        content=request.getPage(self.sourcelink[0])
        if content!=False:
            self.extract(content)

    def createDocuments(self):
        documents=[]
        date=self.intelligence[0]
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
                          'type':getType(self.type),
                          'description': __info__,
                          'by': self.by,
                          'risk': 9,
                    }]
            }
            documents.append(intelligence)
        return documents

    def extract(self,content):
        maincontent = request.getPage(self.sourcelink[1])
        date=datetime.datetime.now().date().__str__()
        if maincontent != False:
            self.log.info("Date information is not availabe")
        else:
            soup = BeautifulSoup(maincontent, 'html.parser')
            block = soup.find('div', class_='download')
            items = block.findAll('p', class_='information')
            date=parser.parser(items[4][14:])
        
        self.intelligence.append(date)
        for line in content:
            if not line or line.startswith('#'):
                continue
            else:
                self.intelligence.append(line.strip("\n"))



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



a=Grensnow()
print(a.checkstatus())
a.getIntelligent()
a.insertdb()













