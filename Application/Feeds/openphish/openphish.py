import  Database.dbmanagment as Dbmanage

import requests
import urllib
import datetime
import  bs4


from Feeds.feeder import Feeder
import Feeds.constants as C
from io import StringIO

description = """
    openphish feeds,
    openphish delivers a list of suspected phishing URLs. Their data comes from affrical intelligent
    this module dowloand feed from openphish,then insertDb


"""


class Feederopenphish(Feeder):

    def __init__(self, type, name,by,description=description,sourcelink=C.Const.openphish.s_link,updateinterval=C.Const.openphish.u_interval):
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

    def getitemsindict(self,item):
        listdict = []
        for i in self.intelligence:
            temp = {
                "_id": i[0],
                "lastDate":  datetime.datetime.utcnow(),
                "type": C.getType(self.type),
                "description": 'Not avvailable',
                "by": self.by,
                "Intelligence":
                    [{
                        "phish_id":i[0],
                        "lastDate": datetime.datetime.utcnow(),
                         "type": C.getType(self.type),
                         "description": i[1],
                         "by": self.by,
                         "online":i[2],
                         "target":i[1],
                         "verified":'Yes',
                         "levelofrisk":"Hight"
                    }]
            }
            listdict.append(temp)
        return listdict


    def extract(self,data,flag=True):
        buffer = StringIO(str(data,'utf-8'))
        for item in buffer:
            temp=None
            if flag:
                r1 = self.getTitleUrl(item)
                temp = [item, r1[0], r1[1]]
            else:
                temp = [item, 'No info','No info']

            print(temp)
            self.intelligence.append(temp)
        print(self.intelligence)

    def getTitleUrl(self,url):
        result=[]         #[title,availeble]
        try:
            page = urllib.request.urlopen(url,timeout=3)
            title = bs4.BeautifulSoup(page.read(), 'html.parser').title.text         # TODO Create final http header  for all feeders to use parser web page
            result=[title,'yes']
        except urllib.error.HTTPError as e:
            result = ['eriselemiyor', 'no' ]
        except urllib.error.URLError as e:
            result = ['eriselemiyor', 'no']
        except Exception as e:
            self.log.error(repr(e))
            result = ['Not found', 'yes']
        return result




    def insertmanydb(self):
        client = Dbmanage.DbClient()
        client.setdatabase('intelligence')
        client.setcollection('url')
        client.insertmany(self.getitemsindict(self.intelligence))

    def insertonedb(self,item):
        client = Dbmanage.DbClient()
        client.setdatabase('intelligence')
        client.setcollection('url')
        client.getdocuments()
        client.insert(
            {
                "_id": item[0],
                "lastDate": datetime.datetime.utcnow(),
                "type": C.getType(self.type),
                "description": 'Not avvailable',
                "by": self.by,
                "Intelligence":
                    [{
                        "phish_id": item[0],
                        "lastDate": datetime.datetime.utcnow(),
                        "type": C.getType(self.type),
                        "description": item[1],
                        "by": self.by,
                        "online": item[2],
                        "target": item[1],
                        "verified": 'Yes',
                        "levelofrisk": "Hight"
                    }]
            }
        )

    def __str__(self):
        return "%s  %s  %s " % (self.name, self.type, self.by)



a=Feederopenphish(C.Type.Phisingurl,"Phishing  Url","OpenPhish",)

#print(a.checkstatus())
a.getIntelligent()
a.insertmanydb()




#curl -d "url=http://checkfb-login404inc.esy.es/recovery-chekpoint-login.html&format=json&app_key=9c6f6c909a9df44bae577bcdf35d97ff87a4d07ef4243db534c8775be81cdc31" http://checkurl.phishtank.com/checkurl/








