from dbmanagment.dbmanagment import DbClient
from constants.values import *
from constants.settings import  RISK
from feeds.feedparent import FeederParent
import core.common as request
import csv

from dateutil import parser

_name_ = "sans_domains"
__by__ = "SANS ICS Suspicious Domains"
__info__ = "blacklist domain feeder"
__collection__="domain"


class Sansdomain(FeederParent):
    __type__ = Type.Domain

    def __init__(self,type=__type__, name=_name_, by=__by__, sourcelink=Feeders.sans_domains.s_link, updateinterval=Feeders.sans_domains.u_interval):
        FeederParent.__init__(self, type, name, by)
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.updateinterval=updateinterval
        self.log=getlog()

    def checkstatus(self,urls=Feeders.sans_domains.s_link):
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
            for  i in item['data']:
                intelligence = {
                    '_id': i,
                    "lastDate": date,
                    'type': getType(self.type),
                    'description': __info__,
                    'by': self.by,
                    'risk': RISK[index],
                    "Intelligence":
                        [{
                            "lastDate": date,
                            "datechunk": [date],
                            'type': getType(self.type),
                            'description': __info__,
                            'source': _name_,
                            'by': self.by,
                            'risk': RISK[index]
                        }]
                }
                documents.append(intelligence)

        return documents

    def extract(self, data,index=0):
        self.intelligence.append({'time':'no info','data':[]})
        readCSV = csv.reader(data)
        for item in readCSV:
            if item[0][0] == "#":
                if 'updated:' in item[0]:
                    time = item[0].rpartition('updated:')[2]
                    self.intelligence[index]['time'] = time
                pass
            else:
                self.intelligence[index]['data'].append(item[0])

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

#a = Sansdomain()
#print(a.checkstatus(a.sourcelink))
#a.getIntelligent()
#a.insertdb()