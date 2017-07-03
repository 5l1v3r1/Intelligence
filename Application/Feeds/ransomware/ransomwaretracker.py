import  Database.dbmanagment as Dbmanage

import requests
import traceback

from Feeds.feeder import Feeder
import Feeds.constants as C
from io import StringIO
from bs4 import  BeautifulSoup
description = """
    RamsomwareTracker feeds,
    RamsomwareTracker ensure  url,domain and ip of  various malwares .



"""


class Feederransomwre(Feeder):

    def __init__(self, type, name,by,description=description,sourcelink=C.Const.ransomware.s_link,updateinterval=C.Const.ransomware.u_interval):
        Feeder.__init__(self,type,name,by)
        self.description=description
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.updateinterval=updateinterval
        self.log=C.getlog()

    def checkstatus(self,url):
        try:
            return self.url_ok(url)  #link is available
        except Exception as e:
            self.log.error(repr(e))

            return False


    def url_ok(self,url):
        r = requests.head(url)
        return r.status_code == 200

    def getIntelligent(self):

        if self.checkstatus(self.sourcelink):
            self.log.info("source link is available")
            try:
                r = requests.get(self.sourcelink,headers=C.Const.headers)
                if r.status_code == 200:
                    self.parsePage(r.content)
                else:
                    self.log.error('Eror on dowloading intelligent http:'+str(r.status_code))
            except Exception as e:
                self.log.error(repr(e))
                traceback.print_exc()
                return False


    def getType(self,name):
        if "ip" in name.lower():
            return C.Type.Malware_ip
        elif "domain" in name.lower():
            return C.Type.Malware_domain
        elif "url" in name.lower():
            return C.Type.Malware_url
    def parsePage(self,data):

        soup = BeautifulSoup(data, 'html.parser')
        name_box = soup.find_all('table', attrs={'class': 'tableblocklist'})
        #print(name_box[1])
        rows = name_box[1].find_all('tr')[1:]
        # {'collection':'ip','doc':[]}
        for row in rows:
            cells = row.find_all("td")
            r1 = cells[1].text.strip()  # malware name
            r2 = cells[2].text.strip()  # scope
            r3 = cells[3].text.strip()  # type
            r4 = cells[4].text.strip()  # risk
            try:
                r5 = cells[5].find('a').get('href')  # link
            except:
                continue
            result=self.extract(r5)
            data=[result,r1,r2,r3,r4,r5]
            if result==-1:
                self.log.error('Eror on gathering intelligent from:' + r5)
            else:
                temp=self.createDocument(data)
                self.intelligence.append({'collection':r3,'doc':temp})

        #print(document)


    def createDocument(self,data):
        date=data[0][0]
        source=data[0][1]
        listdict = []
        for item in source:
            intelligence = {
                '_id': item,
                "lastDate": date,
                'scope': data[2],
                'type': C.getType(self.getType(data[3])),
                'description': data[2],
                'by': self.by,
                'risk': data[4],
                "Intelligence":
                    [{
                        "malware_name": data[1],
                        "lastDate": date,
                        'scope': data[2],
                        'type': C.getType(self.getType(data[3])),
                        'description': data[2],
                        "by": self.by,
                        'risk': data[4]
                    }]

            }
            listdict.append(intelligence)
        return listdict



    def extract(self,url):
        url='http://ransomwaretracker.abuse.ch'+url
        if self.checkstatus(url):
            try:
                r = requests.get(url, headers=C.Const.headers)
                if r.status_code == 200:

                    buffer = StringIO(str(r.content, 'utf-8'))
                    list = [item for item in buffer]
                    date = list[2][15:35]

                    result = []

                    for i in list:
                        if i[0] == '#':
                            continue
                        result.append(i[:-1])

                    if len(result)==0:
                        return -1
                    return [date,result]

                else:
                    self.log.error('Eror on dowloading intelligent http:' + str(r.status_code))
                    return -1
            except Exception as e:
                self.log.error(repr(e))
                return -1









    def insertmanydb(self):
        client = Dbmanage.DbClient()
        client.setdatabase('intelligence')
        for intel in self.intelligence:
            client.setcollection(C.getCollectName(self.getType(intel['collection'])))
            client.insertmany(intel['doc'])

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



a=Feederransomwre(C.Type.Ransomware,"Ransomware  Malware","RamsomwareTracker",)
print(a.checkstatus(a.sourcelink))
a.getIntelligent()
a.insertmanydb()




#curl -d "url=http://checkfb-login404inc.esy.es/recovery-chekpoint-login.html&format=json&app_key=9c6f6c909a9df44bae577bcdf35d97ff87a4d07ef4243db534c8775be81cdc31" http://checkurl.phishtank.com/checkurl/







