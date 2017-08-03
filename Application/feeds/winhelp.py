
from dbmanagment.dbmanagment import DbClient
from constants.values import *
from feeds.feedparent import FeederParent
import core.common as request
import datetime
from dateutil import parser

_name_ = "winhwlp"
__by__ = "Winhelp Suspicious Domains"
__info__ = "blacklist domain feeder"
__collection__="domain"
__lastdate__ = datetime.datetime.now()
__type__ = Type.Domain
class Winhelp(FeederParent):


    def __init__(self,type=__type__, name=_name_,by=__by__,sourcelink=Feeders.winhelp.s_link,updateinterval=Feeders.winhelp.u_interval):
        FeederParent.__init__(self,type,name,by)
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.updateinterval=updateinterval
        self.log=getlog()

    def checkstatus(self,urls=Feeders.winhelp.s_link):
            temp=request.checkstatus(urls)
            self.log.info("Source Available-> "+str(urls)+" :"+str(temp))

    def getIntelligent(self):
        if type(self.sourcelink)==type([]):
            for item in self.sourcelink:
                content = request.getPage(item)
                if content != False:
                    self.extract(content)
                else:
                    self.log.info("Page not available-> "+item)
        else:
            content=request.getPage(self.sourcelink)
            if content!=False:
                self.extract(content)


    def createDocuments(self):
        documents = []
        for index,item in enumerate(self.intelligence):
            time = item['time']
            date=parser.parse(time)
            for  i in item['data']:
                intelligence = {
                    '_id': i,
                    "lastDate": date,
                    'type': getType(self.type),
                    'description': __info__,
                    'by': self.by,
                    'risk': 8,
                    "Intelligence":
                        [{
                            "lastDate": date,
                            "datechunk": [date],
                            'type': getType(self.type),
                            'description': __info__,
                            'source': _name_,
                            'by': self.by,
                            'risk': 8
                        }]
                }
                documents.append(intelligence)
        return documents

    def extract(self, data,index=0):
        self.intelligence.append({'time':'no info','data':[]})
        for item in data:
            if item[0] == "#" or len(item) == 2 :
                for a in item.split():
                    if a == "Updated:":
                        time = item.rpartition('Updated:')[2].rpartition(' ')[0].rpartition(' ')[0]
                        self.intelligence[index]['time'] = time
                pass
            else:
                        b = item.split()
                        self.intelligence[index]['data'].append(b[1])
        print(len(self.intelligence))

        self.intelligence[index]['data'] = list(set(self.intelligence[index]['data']))


    def insertdb(self):
        if len(self.intelligence)>=1:
            client = DbClient()
            client.set_database('intelligence')
            client.set_collection(__collection__)
            client.insert_many(self.createDocuments())
        else:
            self.log.info("Intelligece empty")

    def __str__(self):
        return "%s  %s  %s " % (self.name, self.type, self.by)

#a = Winhelp()
#print(a.checkstatus(a.sourcelink))
#a.getIntelligent()
#a.insertdb()