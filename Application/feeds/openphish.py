from  dbmanagment.dbmanagment import DbClient
import urllib
import datetime
import  bs4

import core.common as request
from constants.values import *
from feeds.feedparent import FeederParent




_name_ = "Openphish feeds"
__by__ = "Openphish"
__info__ = "openphish delivers a list of suspected phishing URLs. Their data comes from affrical intelligent"
__collection__="url"


class Openphish(FeederParent):              #todo this run very slowly therefore modify this feeder,it will be multhiread
    __type__ = Type.Phisingurl
    def __init__(self,type=__type__, name=_name_,by=__by__,description=__info__,sourcelink=Feeders.openphish.s_link,updateinterval=Feeders.openphish.u_interval):
        FeederParent.__init__(self,type,name,by)
        self.description=description
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.updateinterval=updateinterval
        self.log=getlog()



    def checkstatus(self,url=Feeders.openphish.s_link):
        return request.checkstatus(url)  #link is available

    def getIntelligent(self):
        content=request.getPage(self.sourcelink)
        if content!=False:
            self.extract(content)



    def getitemsindict(self,item):
        listdict = []
        for i in self.intelligence:
            temp = {
                "_id": i[0],
                "lastDate":  datetime.datetime.utcnow(),
                "type": getType(self.type),
                "description": 'Not avvailable',
                "by": self.by,
                "Intelligence":
                    [{
                        "phish_id":i[0],
                        "lastDate": datetime.datetime.utcnow(),
                         "type": getType(self.type),
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


    def extract(self,data,flag=False):
        for item in data:
            temp=None
            if flag:
                r1 = self.getTitleUrl(item)
                temp = [item, r1[0], r1[1]]
            else:
                temp = [item, 'No info','No info']

            #print(temp)
            self.intelligence.append(temp)
        print("Total intelligence %d"%len(self.intelligence))

    def getTitleUrl(self,url):
        result=[]         #[title,availeble]
        try:
            page = urllib.request.urlopen(url,timeout=3)
            title = bs4.BeautifulSoup(page.read(), 'html.parser').title.text
            result=[title,'yes']
        except urllib.error.HTTPError as e:
            result = ['eriselemiyor', 'no' ]
        except urllib.error.URLError as e:
            result = ['eriselemiyor', 'no']
        except Exception as e:
            self.log.error(repr(e))
            result = ['Not found', 'yes']
        return result




    def insertdb(self):
        client = DbClient()
        client.setdatabase('intelligence')
        client.setcollection('url')
        client.insertmany(self.getitemsindict(self.intelligence))

    def insertonedb(self,item):
        client = DbClient()
        client.setdatabase('intelligence')
        client.setcollection('url')
        client.getdocuments()
        client.insert(
            {
                "_id": item[0],
                "lastDate": datetime.datetime.utcnow(),
                "type": getType(self.type),
                "description": 'Not avvailable',
                "by": self.by,
                "Intelligence":
                    [{
                        "phish_id": item[0],
                        "lastDate": datetime.datetime.utcnow(),
                        "type": getType(self.type),
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



#a=Openphish(Type.Phisingurl,"Phishing  Url","OpenPhish",)

#print(a.checkstatus())
#a.getIntelligent()
#a.insertmanydb()




#curl -d "url=http://checkfb-login404inc.esy.es/recovery-chekpoint-login.html&format=json&app_key=9c6f6c909a9df44bae577bcdf35d97ff87a4d07ef4243db534c8775be81cdc31" http://checkurl.phishtank.com/checkurl/








