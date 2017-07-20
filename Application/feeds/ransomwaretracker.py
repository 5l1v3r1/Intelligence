import requests
import traceback
from constants.settings import HEADERS, RISK
from dbmanagment.dbmanagment import DbClient
from constants.values import *
import core.common as request
from feeds.feedparent import FeederParent
from dateutil import parser
from io import StringIO
from bs4 import  BeautifulSoup


_name_ = "RamsomwareTracker"
__by__ = "RamsomwareTracker"
__info__ = "RamsomwareTracker ensure  url,domain and ip of  various malwares"


class Ransomware(FeederParent):
    __type__ = Type.Ransomware
    def __init__(self, type=__type__, name=_name_, by=__by__, description=__info__, sourcelink=Feeders.ransomware.s_link, updateinterval=Feeders.ransomware.u_interval):
        FeederParent.__init__(self, type, name, by)
        self.description=description
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.updateinterval=updateinterval
        self.log=getlog()

    def checkstatus(self, url=Feeders.ransomware.s_link):
        return request.checkstatus(url)  # link is available



    def getIntelligent(self):

        if self.checkstatus(self.sourcelink):
            self.log.info("source link is available")
            try:
                r = requests.get(self.sourcelink,headers=HEADERS)
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
            return Type.Malware_ip
        elif "domain" in name.lower():
            return Type.Malware_domain
        elif "url" in name.lower():
            return Type.Malware_url

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
        date = parser.parse('2017-07-19 22:28:23.772')
        source=data[0][1]
        listdict = []
        for item in source:
            intelligence = {
                '_id': item,
                "lastDate": date,
                'scope': data[2],
                'type': getType(self.getType(data[3])),
                'description': data[2],
                'by': self.by,
                'risk': RISK[data[4].lower()],
                "Intelligence":
                    [{
                        "malware_name": data[1],
                        "lastDate": date,
                        "datechunk":[date],
                        'scope': data[2],
                        'type': getType(self.getType(data[3])),
                        'description': data[2],
                        "by": self.by,
                        'risk': RISK[data[4].lower()]
                    }]

            }
            listdict.append(intelligence)
        return listdict

    def extract(self,url):
        url='http://ransomwaretracker.abuse.ch'+url
        if self.checkstatus(url):
            try:
                r = requests.get(url, headers=HEADERS)
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

    def insertdb(self):
        client = DbClient()
        client.set_database('intelligence')
        for intel in self.intelligence:
            client.set_collection(getCollectName(self.getType(intel['collection'])))
            client.insert_many(intel['doc'])


    def __str__(self):
        return "%s  %s  %s " % (self.name, self.type, self.by)

#a=Ransomware(Type.Ransomware,"Ransomware  Malware","RamsomwareTracker",)
#print(a.checkstatus(a.sourcelink))
#a.getIntelligent()
#a.insertdb()