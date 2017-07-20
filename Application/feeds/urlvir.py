from  dbmanagment.dbmanagment import DbClient
from feeds.feedparent import FeederParent
import core.common as request
from constants.values import *
from dateutil import parser



_name_ = "URLVir"
__by__ = "URLVir by NoVirusThanks "
__info__ = "Malicious Executable URLs"
__collection__={0:'ip',1:'domain'}
__reference__ = "NoVirusThanks"

class Urlvir(FeederParent):
    __type__ ={0:Type.Ip,1:Type.Domain}
    def __init__(self, type=__type__, name=_name_, by=__by__, sourcelink=Feeders.urlvir.s_link, updateinterval=Feeders.urlvir.u_interval):
        FeederParent.__init__(self, type, name, by)
        self.intelligence = []
        self.sourcelink = sourcelink
        self.info = __info__
        self.updateinterval = updateinterval
        self.log = getlog()

    def checkstatus(self, urls=Feeders.urlvir.s_link):
        for item in urls:
            temp = request.checkstatus(item)
            self.log.info("Source Available-> " + str(item) + " :" + str(temp))

    def getIntelligent(self):
        if type(self.sourcelink) == type([]):
            for index, item in enumerate(self.sourcelink):
                content = request.getPage(item)
                if content != False:
                    self.extract(content)
                else:
                    self.log.info("Page not available-> " + item)
        else:
            content = request.getPage(self.sourcelink)
            if content != False:
                self.extract(content)

    def createDocuments(self,index,data=None):
        documents = []
        date=parser.parse(data[0])
        for item in data[1:]:
            intelligence = {
                '_id': item,
                "lastDate": date,
                'type':getType(self.type[index]),
                'description': __info__,
                'by': self.by,
                'risk': 8,
                "Intelligence":
                    [{
                          'lastDate': date,
                          'datechunk': [date],
                          'type':getType(self.type[index]),
                          'description': __info__,
                          'by': self.by,
                          'risk': 8,
                    }]
            }
            documents.append(intelligence)
        return documents

    def extract(self, content):
        temp=[]
        for line in content:
            if line.startswith('#') or not line:
                if line.startswith('#Updated on'):
                    date=line.split('#Updated on ')[1]
                    date=date.strip()
                    temp.append(date)
            else:
                a=line.strip('\n')
                temp.append(a)

        self.intelligence.append(temp)

    def insertdb(self):

        client = DbClient()
        client.set_database('intelligence')
        for index,intel in enumerate(self.intelligence):
            client.set_collection(__collection__[index])
            client.insert_many(self.createDocuments(index,intel))

    def __str__(self):
        return "%s  %s  %s " % (self.name, self.type, self.by)

#a=Urlvir()
#a.checkstatus(a.sourcelink)
#a.getIntelligent()
#a.insertdb()



