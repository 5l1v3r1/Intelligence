import  Database.dbmanagment as Dbmanage

import requests
import json

from Feeds.feeder import Feeder
import Feeds.constants as C
from io import StringIO

description = """
    phishTank feeds,
    PhishTank delivers a list of suspected phishing URLs. Their data comes from human reports
    this module dowloand feed from phinsTank,then insertDb


"""


class Feederphistank(Feeder):

    def __init__(self, type, name,by,description=description,sourcelink=C.Const.phistank.s_link,updateinterval=C.Const.phistank.u_interval):
        Feeder.__init__(self,type,name,by)
        self.description=description
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.updateinterval=updateinterval
        self.log=C.getlog()

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
                "_id": i[1],
                "lastDate": i[3],
                "type": C.getType(self.type),
                "description": i[2],
                "by": self.by,
                "Intelligence":
                    [{
                        "phish_id":i[0],
                        "lastDate": i[3],
                         "type": C.getType(self.type),
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

        buffer = StringIO(str(data,'utf-8'))
        readCSV = csv.reader(buffer, delimiter=',')
        for item in readCSV:
                self.intelligence.append(item)
        #print(self.intelligence)

    def validateUrl(self,url):
        payload = {'url': url, 'format': 'json','app_key':C.Const.phistank.app_key}
        response = requests.post(C.Const.phistank.api_link, data=payload)
        d = json.loads(response.text)
        return d







    def insertmanydb(self):
        client = Dbmanage.DbClient()
        client.setdatabase('intelligence')
        client.setcollection('url')
        client.insertmany(self.getitemsindict())

    def insertonedb(self,item):
        client = Dbmanage.DbClient()
        client.setdatabase('intelligence')
        client.setcollection('url')
        client.getdocuments()
        client.insert(
            {
                "_id": item[1],
                "lastDate": item[3],
                "type": C.getType(self.type),
                "description": item[2],
                "by": self.by,
                "Intelligence":
                    [{
                        "phish_id":item[0],
                        "lastDate": item[3],
                         "type": C.getType(self.type),
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



a=Feederphistank(C.Type.Phisingurl,"Phishing  Url","PhishTank",)
a.validateUrl('http://checkfb-login404inc.esy.es/recovery-chekpoint-login.html')
#print(a.checkstatus())
#a.getIntelligent()
#a.insertmanydb()




#curl -d "url=http://checkfb-login404inc.esy.es/recovery-chekpoint-login.html&format=json&app_key=9c6f6c909a9df44bae577bcdf35d97ff87a4d07ef4243db534c8775be81cdc31" http://checkurl.phishtank.com/checkurl/








