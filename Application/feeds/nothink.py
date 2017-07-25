from dbmanagment.dbmanagment import DbClient
from constants.values import *
from constants.settings import  RISK
from feeds.feedparent import FeederParent
import core.common as request


from dateutil import parser

_name_ = "nothink"
__by__ = "Nothink Suspicious Ip adresses"
__collection__="ip"
__reference__="Honeypot"

class Nothink(FeederParent):
    __type__ = Type.Ip

    def __init__(self,type=__type__, name=_name_, by=__by__, sourcelink=Feeders.nothink.s_link, updateinterval=Feeders.nothink.u_interval):
        FeederParent.__init__(self, type, name, by)
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.updateinterval=updateinterval
        self.log=getlog()

    def checkstatus(self,urls=Feeders.nothink.s_link):
        for item in urls:
            temp=request.checkstatus(item)
            self.log.info("Source Available-> "+str(item)+" :"+str(temp))

    def getIntelligent(self):
        if type(self.sourcelink) == type([]):
            for index,item in enumerate(self.sourcelink):
                content = request.getPage(item)
                if content != False:
                    self.extract(content,index)
                else:
                    self.log.info("Page not available-> "+item)
        else:
            content=request.getPage(self.sourcelink)
            if content!=False:
                self.extract(content)


    def createDocuments(self):
        documents=[]
        for index,item in enumerate(self.intelligence):
            time = item['time']
            date=parser.parse(time)
            info = item['info']
            for  i in item['data']:
                intelligence = {
                    '_id': i,
                    "lastDate": date,
                    'type': getType(self.type),
                    'description': info,
                    'by': self.by,
                    'risk': 9,
                    "Intelligence":
                        [{
                            "lastDate": date,
                            "datechunk": [date],
                            'type': getType(self.type),
                            'description': info,
                            'source': _name_,
                            'by': self.by,
                            'risk': 9
                        }]
                }
                documents.append(intelligence)

        return documents

    def extract(self, data,index=0):
        self.intelligence.append({'info':'no info','time':'no info','data':[]})
        for item in data:
            if item[0] == "#":
                if 'Generated' in item:
                    time = item.rpartition('Generated')[2]
                    self.intelligence[index]['time'] = time[:-1]
                elif 'blacklist' in item:
                    info = item.rpartition(',')[0]
                    self.intelligence[index]['info'] = info[2:]
            else:
                self.intelligence[index]['data'].append(item)

    def insertdb(self):
        if len(self.intelligence) > 1:
            client = DbClient()
            client.set_database('intelligence')
            client.set_collection(__collection__)
            client.insert_many(self.createDocuments())
        else:
            self.log.info("Intelligece empty")

    def __str__(self):
        return "%s  %s  %s " % (self.name, self.type, self.by)

a = Nothink()
print(a.checkstatus(a.sourcelink))
a.getIntelligent()
a.insertdb()