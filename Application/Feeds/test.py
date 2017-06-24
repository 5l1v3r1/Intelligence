import urllib.request
import csv
import requests

from abc import ABC, abstractmethod
import Feeds.constants as C


def getItemDictionary(items):
    print("Hello")
    listdict=[]
    for i in items:
        temp={
            "_id": i[0],
            "lastDate": i[1],
            "type": "BlackIP",
            "description": i[2],
            "by": "Cyber Struggle",
            "Intelligence":
                [{
                    "lastDate": i[1],
                    "type": "BlackIP",
                    "description": i[2],
                    "by": "Cyber Struggle",
                    "confidence": "alahaemanet"
                }]
        }
        listdict.append(temp)
    print(listdict)

items=[['186.248.147.235','2017-06-23 01:10:35.063',"Incoming Masscan detected"],
       ['1.246.101.246','2017-06-23 01:08:44.433',"RA SCAN Unusually fast Terminal Server Traffic Inbound"],
       ['5.3.173.102','2017-06-23 01:08:44.680',"source disclosure vulnerability"],
       ['5.8.48.21','2017-06-23 01:08:44.922',"MS Terminal Server scanner taffic on Non-standard Port"],
       ['5.10.171.122', '2017-06-23 01:08:45.428', "RA SCAN Unusually fast Terminal Server Traffic Inbound"],
       ['223.202.204.137', '2017-06-23 01:11:00.879', "SSH Brute Force"],
       ['223.85.149.108', '2017-06-23 01:11:00.605', "Possible Apache Struts OGNL Expression Injection (CVE-2017-5638) M2"],
       ['222.186.51.49', '2017-06-23 01:11:00.015', "Microsoft Remote Desktop (RDP) Syn then Reset 30 Second DoS Attempt"],
       ]

