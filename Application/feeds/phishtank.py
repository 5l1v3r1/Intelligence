from  dbmanagment.dbmanagment import DbClient

import requests
import json
import csv


from constants.values import *
import core.common as request


description = """
    phishTank feeds,
    PhishTank delivers a list of suspected phishing URLs. Their data comes from human reports
    this module dowloand feed from phinsTank,then insertDb


"""
__url__ = "http://data.phishtank.com/data/online-valid.csv"
__name__ = "PhishTank"
__by__ = "phishTank"
__info__ = "PhishTank delivers a list of suspected phishing URLs. Their data comes from human reports "
__collection__="url"



class Feederphistank(Feeder):
    __type__ = Type.Phisingurl
    def __init__(self, type=__type__, name=__name__, by=__by__, description=__info__,sourcelink=Feeders.phistank.s_link,updateinterval=Feeders.phistank.u_interval):
        Feeder.__init__(self,type,name,by)
        self.description=description
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.updateinterval=updateinterval
        self.log=getlog()


    def checkstatus(self, url=__url__):
        return request.checkstatus(url)  # link is available


    def getIntelligent(self):
        content=request.getPage(self.sourcelink)
        if content!=False:
            self.extract(content)


    def getitemsindict(self,):
        listdict = []
        for i in self.intelligence:
            temp = {
                "_id": i[1],
                "lastDate": i[3],
                "type": getType(self.type),
                "description": i[2],
                "by": self.by,
                "Intelligence":
                    [{
                        "phish_id":i[0],
                        "lastDate": i[3],
                         "type": getType(self.type),
                         "description": i[2],
                         "by": self.by,
                         "online":i[6],
                         "target":i[7],
                         "verified":i[4],
                         "verification_time": i[5],
                         "levelofrisk":"Hight"
                    }]
            }
            listdict.append(temp)
        return listdict


    def extract(self,data):

        readCSV = csv.reader(data, delimiter=',')
        for item in readCSV:
                self.intelligence.append(item)


    def validateUrl(self,url):
        payload = {'url': url, 'format': 'json','app_key':Feeders.phistank.app_key}
        response = requests.post(Feeders.phistank.api_link, data=payload)
        d = json.loads(response.text)
        return d







    def insertdb(self):
        client = DbClient()
        client.setdatabase('intelligence')
        client.setcollection(__collection__)
        client.insertmany(self.getitemsindict())

    def insertonedb(self,item):
        client = DbClient()
        client.setdatabase('intelligence')
        client.setcollection('url')
        client.getdocuments()
        client.insert(
            {
                "_id": item[1],
                "lastDate": item[3],
                "type": getType(self.type),
                "description": item[2],
                "by": self.by,
                "Intelligence":
                    [{
                        "phish_id":item[0],
                        "lastDate": item[3],
                         "type": getType(self.type),
                         "description": item[2],
                         "by": self.by,
                         "online":item[6],
                         "target":item[7],
                         "verified":item[4],
                         "verification_time": item[5],
                         "levelofrisk":"Hight"
                    }]
            }
        )

    def __str__(self):
        return "%s  %s  %s " % (self.name, self.type, self.by)



a=Feederphistank(Type.Phisingurl,"Phishing  Url","PhishTank",)
#a.validateUrl('http://checkfb-login404inc.esy.es/recovery-chekpoint-login.html')
print(a.checkstatus())
a.getIntelligent()
a.insertdb()




#curl -d "url=http://checkfb-login404inc.esy.es/recovery-chekpoint-login.html&format=json&app_key=9c6f6c909a9df44bae577bcdf35d97ff87a4d07ef4243db534c8775be81cdc31" http://checkurl.phishtank.com/checkurl/







