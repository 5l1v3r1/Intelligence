import urllib.request
import csv
import requests

from abc import ABC, abstractmethod
import Feeds.constants as C



def url_ok(url):
    r = requests.head(url)
    print(r)
    return r.status_code == 200

r = requests.get('https://www.autoshun.org/download/?api_key=d4066260862da9118d84717e17c0fc&format=csv')
print(r)


req = urllib.request.urlopen('https://www.autoshun.org/download/?api_key=d4066260862da9118d84717e17c0fc&format=csv')

data = req.read()
print(data)
readCSV = csv.reader(data, delimiter=',')
result = []
for item in readCSV:
    if item[0][0] == "#":
        print("Pass ")
    else:
        print(item[0], item[1], item[2])
        result.append(item)

print(result)
# Write data to file
#filename = "autoshun.csv"
#file_ = open(filename, 'w')
#file_.write(data)
#file_.close()

