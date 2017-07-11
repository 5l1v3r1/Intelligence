from  dbmanagment.dbmanagment import DbClient

import core.common as request
import csv
from constants.values import *

from feeds.feedparent import FeederParent

description = """
    autoshun feeds,
    it gets all Intelligent from autoshon list,then insert database

    ->CSV stands for "comma-separated values". Its data fields are most often separated, or delimited, by a comma.


"""


_name_ = "autoshun_feeds"
__by__ = "autoshun"
__info__ = "it gets all Intelligent from autoshon list,then insert database "
__collection__="ip"



class Autoshun(FeederParent):
    __type__ = Type.Ip
    def __init__(self, type=__type__, name=_name_,by=__by__,description=__info__,sourcelink=Feeders.autoshun.s_link,updateinterval=Feeders.autoshun.u_interval):
        FeederParent.__init__(self,type,name,by)
        self.description=description
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.updateinterval=updateinterval
        self.log=getlog()

    def checkstatus(self, url=Feeders.autoshun.s_link):
        return request.checkstatus(url)  # link is available


    def getIntelligent(self):
        content = request.getPage(self.sourcelink)
        if content != False:
            self.extract(content)
        else:
            self.log.info("Content is empty.Failed retriveing intelligent")

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
        readCSV = csv.reader(data, delimiter=',')
        for item in readCSV:
            if item[0][0] == "#":
                pass
            else:
                self.intelligence.append(item)
                # print(self.intelligence)





    def insertdb(self):
        if len(self.intelligence)==0:
            self.log.error("Intelligent data is empty")
            return False;
        client = DbClient()
        client.setdatabase('intelligence')
        client.setcollection(__collection__)
        client.insertmany(self.getitemsindict())

    def insertonedb(self,item):
        client = DbClient()
        client.setdatabase('intelligence')
        client.setcollection(__collection__)
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

if __name__ == '__main__':
    # This won't work!
    print("here")
#a=Autoshun(Type.Ip,"Autoshun","Autshun","adad")
#print(a.checkstatus(a.sourcelink))
#a.getIntelligent()
#a.insertdb()














