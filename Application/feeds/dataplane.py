from  dbmanagment.dbmanagment import DbClient



from feeds.feedparent import FeederParent
import core.common as request
from constants.values import *
from dateutil import parser



_name_ = "DataPlane"
__by__ = "DataPlane.org"
__info__ = "DataPlane.org is a community-powered Internet data, feeds, and measurement resource for operators, by operators. We provide reliable and trustworthy service at no cost."
__collection__="ip"

category={'dnsrd':['sending recursive DNS queries to a remote host,may be open DNS resolvers or evaluating cache entries',6],
          'dnsrdany':['recursive DNS IN ANY queries to a remote host. May be open DNS resolvers',6],
           'dnsversion':['identified as sending DNS CH TXT VERSION.BIND queries to a remote host',6],
          'sipinvitation': ['SIP INVITE operation to a remote host,suspicious of more than just port scanning,These hosts may be SIP client cataloging or conducting various forms of telephony abuse',8],
          'sipquery': ['SIP OPTIONS query to a remote host,suspicious of more than just port scanningThese hosts may be SIP,client cataloging or conducting various forms of telephony abuse', 8],
          'sipregistration':['a SIP REGISTER query to a remote host,suspicious of more than just port scanning,These hosts may be SIP client cataloging or conducting various forms of telephony abuse', 8],
          'sshclient': ['an SSH connection to a remote host,SSH server cataloging or conducting authentication attack attempts', 8],
          'sshpwauth': ['attempting to remotely login to a host using SSH password authentication', 10],
          'vncrfb': ['VNC remote frame buffer (RFB) session to a remote host,remote access abuse', 6],
          }



class Dataplane(FeederParent):
    __type__ = Type.Ip
    def __init__(self, type=__type__, name=_name_,by=__by__,sourcelink=Feeders.datapalane.s_link,updateinterval=Feeders.datapalane.u_interval):
        FeederParent.__init__(self,type,name,by)
        self.intelligence=[]
        self.sourcelink=sourcelink
        self.info=__info__
        self.updateinterval=updateinterval
        self.log=getlog()                           #this comming from constans

    def checkstatus(self,urls=Feeders.datapalane.s_link):
        for item in urls:
            temp=request.checkstatus(item)
            self.log.info("Source Available-> "+str(item)+" :"+str(temp))


    def getIntelligent(self):
        if type(self.sourcelink)==type([]):
            for item in self.sourcelink:
                content = request.getPage(item)
                if content != False:
                    self.extract(content)
                else:
                    self.log.info("Page not available-> "+item)

        else:
            content=request.getPage(self.sourcelink)
            if content!=False:
                self.extract(content)

    def createDocuments(self):
        # DstIP,DstPort,count
        documents = []
        for item in self.intelligence[1:]:
            intelligence = {
                '_id': item[1],
                "lastDate": parser.parse(item[2]),
                'type':getType(self.type),
                'category':item[3],
                'description': category[item[3]][0],
                'by': self.by,
                'risk': category[item[3]][1],
                "Intelligence":
                    [{
                        "lastDate": parser.parse(item[2]),
                        'type': getType(self.type),
                        'category': item[3],
                        'networkname': item[0],
                        'description': category[item[3]][0],
                        'by': self.by,
                        'risk': category[item[3]][1],
                    }]

            }
            documents.append(intelligence)
        return documents

    def extract(self,content):
        for line in content:
            if line.startswith('#') or not line:
               pass
            else:
                item=line.split('|')
                self.intelligence.append([item[1].strip(),item[2].strip(),item[3].strip(),item[4].strip()]) #ASname,saddr,utc,category
        print(len(self.intelligence))
    def insertdb(self):
        if len(self.intelligence)>1:
            client = DbClient()
            client.setdatabase('intelligence')
            client.setcollection(__collection__)
            client.insertmany(self.createDocuments())
        else:
            self.log.info("Intelligece empty")

    def __str__(self):
        return "%s  %s  %s " % (self.name, self.type, self.by)



a=Dataplane()
a.checkstatus(a.sourcelink)
#a.getIntelligent()
#temp=''

#a.insertdb()











