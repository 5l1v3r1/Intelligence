import  Database.dbmanagment as Dbmanage
import urllib.request
import csv
import requests

from abc import ABC, abstractmethod
import Feeds.constants as C






class Feeder(ABC):


    def __init__(self, type, name,by):
        self.name = name
        self.type=type
        self.by=by


    @abstractmethod
    def checkstatus(self):
        pass

    #def __str__(self):
    #    return "%s  %s  %s " % (self.name, self.type,self.by)

class Feederautoshun(Feeder):

    def __init__(self, type, name,by,description,sourcelink=C.Const.autoshun.s_link,updateinterval=C.Const.autoshun.u_interval):
        Feeder.__init__(self,type,name,by)
        self.description=description
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.updateinterval=updateinterval
        self.log=C.getlog()

    def checkstatus(self):
        try:
            return self.url_ok(self.sourcelink)#link is available
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
                print("zaaa")
                if r.status_code == 200:
                    with open('autoshun.csv', 'wb') as f:
                        f.write(r.content)       # Fixme: THis operation that save file  then read it, most probablity is unneccessariy,Check again
                    self.extract('autoshun.csv')
                elif r.status_code == 304:              # TODO this will be change,it is temprorariy for now
                    self.extract('report.csv')
                else:
                    self.log.error('Eror on dowloading intelligent http:'+str(r.status_code))
            except Exception as e:
                self.log.error(repr(e))
                return False



    def extract(self,data):
        #print(data)
        with open('report.csv') as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for item in readCSV:
                if item[0][0] == "#":
                    print("Pass ")
                else:
                    #print(item[0], item[1], item[2])
                    self.intelligence.append(item)
            print(self.intelligence)
    def insertDb(self):
        print("Okey başla eklemeye")
        client = Dbmanage.DbClient(ip='138.68.92.9')

        print(client.databases())
        client.setdatabase('intelligence')
        print(client.collections())
        client.setcollection('ip')
        client.getdocuments()
        #client.delete('594a740fde163924ae0cd1d9')
        for item in self.intelligence:
            client.insert(
                {
                    "_id":item[0],
                    "lastDate": item[1],
                    "type":"BlackIP",
                    "description": item[2],
                    "by": self.by,
                    "Intelligence":
                    [{
                         "lastDate":  item[1],
                         "type": "BlackIP",
                         "description": item[2],
                         "by": self.by,
                         "confidence": "alahaemanet"
                    }]
                }
            )


    def __str__(self):
        return "%s  %s  %s " % (self.name, self.type, self.by)








a=Feederautoshun(C.Type.Ip,"Autoshun","Autshun","adad")
print(a.checkstatus())
a.getIntelligent()
a.insertDb()
description = """
    autoshun feeds,
    it gets all Intelligent from autoshon list,then insert database
    ->CSV is a simple file format used to store tabular data, such as a spreadsheet or database.
    Files in the CSV format can be imported to and exported from programs that store data in tables,
    such as Microsoft Excel or OpenOffice Calc.

    ->CSV stands for "comma-separated values". Its data fields are most often separated, or delimited, by a comma.


"""













