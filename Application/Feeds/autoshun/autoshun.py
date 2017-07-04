from  dbmanagment.dbmanagment import DbClient
import csv
import requests

from feeds.feeder import Feeder
from constants.values import *

from io import StringIO

description = """
    autoshun feeds,
    it gets all Intelligent from autoshon list,then insert database

    ->CSV stands for "comma-separated values". Its data fields are most often separated, or delimited, by a comma.


"""


class Feederautoshun(Feeder):

    def __init__(self, type, name,by,description,sourcelink=Const.autoshun.s_link,updateinterval=Const.autoshun.u_interval):
        Feeder.__init__(self,type,name,by)
        self.description=description
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.updateinterval=updateinterval
        self.log=getlog()

    def checkstatus(self):
        try:
            return self.url_ok(self.sourcelink)  #link is available
        except Exception as e:
            self.log.error(repr(e))
            return False


    def url_ok(self,url):
        r = requests.head(url)
        return r.status_code == 200

    def getIntelligent(self):

        if self.checkstatus():
            self.log.info("source link is available")
            try:
                r = requests.get(self.sourcelink)
                if r.status_code == 200:
                    self.extract(r.content)
                else:
                    self.log.error('Eror on dowloading intelligent http:'+str(r.status_code))

            except Exception as e:
                self.log.error(repr(e))
                return False

    def getitemsindict(self,):
        listdict = []
        for i in self.intelligence:
            temp = {
                "_id": i[0],
                "lastDate": i[1],
                "type": getType(self.type),
                "description": i[2],
                "by": self.by,
                "Intelligence":
                    [{
                        "lastDate": i[1],
                        "type": getType(self.type),
                        "description": i[2],
                        "by": self.by,
                        "confidence": "alahaemanet"
                    }]
            }
            listdict.append(temp)
        return listdict


    def extract(self,data):
        buffer = StringIO(str(data, 'utf-8'))
        readCSV = csv.reader(buffer, delimiter=',')
        for item in readCSV:
            if item[0][0] == "#":
                pass
            else:
                self.intelligence.append(item)
                # print(self.intelligence)





    def insertmanydb(self):
        if len(self.intelligence)==0:
            self.log.error("Intelligent data is empty")
            return False;
        client = DbClient()
        client.setdatabase('intelligence')
        client.setcollection('ip')
        client.insertmany(self.getitemsindict())

    def insertonedb(self,item):
        client = DbClient()
        client.setdatabase('intelligence')
        client.setcollection('ip')
        client.getdocuments()
        client.insert(
            {
                "_id": item[0],
                "lastDate": item[1],
                "type": getType(self.type),
                "description": item[2],
                "by": self.by,
                "Intelligence":
                    [{
                        "lastDate": item[1],
                        "type":getType(self.type),
                        "description": item[2],
                        "by": self.by,
                        "confidence": "alahaemanet"
                    }]
            }
        )

    def __str__(self):
        return "%s  %s  %s " % (self.name, self.type, self.by)



a=Feederautoshun(Type.Ip,"Autoshun","Autshun","adad")
print(a.checkstatus())
a.getIntelligent()
a.insertmanydb()














