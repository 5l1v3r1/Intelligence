import requests
import urllib.request
from io import StringIO
import requests
import Feeds.constants as C
import datetime
from bs4 import  BeautifulSoup





url='http://ransomwaretracker.abuse.ch/blocklist/'
urldw='http://ransomwaretracker.abuse.ch/downloads/CW_C2_URLBL.txt'
url2='http://www.timeturk.com'



def extract(data):


    buffer = StringIO(str(data, 'utf-8'))
    list = [item for item in buffer]
    #print(list)
    date=list[2][15:35]
    print(date)
    result=[]
    for i in list:
        if i[0]=='#':
            continue
        result.append(i[:-1])

    print(result)

def getIntelligent(url):
    r = requests.get(url)
    extract(r.content)


def parsePage(url):
    result = requests.get(url, headers=C.Const.headers)

    # print(result.content.decode())
    soup = BeautifulSoup(result.content.decode(), 'html.parser')

    name_box = soup.find_all('table', attrs={'class': 'tableblocklist'})
    print(name_box[1])
    rows = name_box[1].find_all('tr')[1:]
    for row in rows:
        cells = row.find_all("td")
        r1=cells[1].text.strip()#malware name
        r2=cells[2].text.strip()#scope
        r3 = cells[3].text.strip()#type
        r4=cells[4].text.strip()#risk
        r5 = cells[5].find('a').get('href')#link


#f = urllib.request.urlopen(url)
#print(f.read().decode('utf-8'))
#req = urllib.request.Request(url,data=b'None',headers={'User-Agent':' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
#handler = urllib.request.urlopen(req)
#print(handler)

parsePage(url)
getIntelligent(urldw)