import requests
from dateutil import parser
import traceback
from constants.values import Feeders,getlog
from constants.settings import HEADERS,TIMEOUT
from io import StringIO
import inspect

_log=getlog()
_allfeeders_=[]



def checkstatus(url):
    try:
        return url_ok(url)  # link is available
    except Exception as e:
        _log.error(repr(e))
        return False


def url_ok( url):
    r = requests.head(url,headers=HEADERS,timeout=TIMEOUT)
    return r.status_code == 200

def getStackdata(number=2):
    stackframe = inspect.stack()[number]
    return  ' ' + stackframe[3] + ' ' + str(stackframe[2]) + ' line ' + stackframe[1].split('/')[-1]


def getPage(url,parameter=None,rtype=0):
    re=None
    try:
        _log.info("Trying  to  connect page "+' [ '+getStackdata()+' ] ')
        re = requests.get(url,headers=HEADERS,timeout=TIMEOUT)
        if re.status_code == 200:
            
            _log.info("Page retrieved  " +' [ '+getStackdata()+' ] ')
            #a=r.headers['content-disposition'] # atachmetn tipini soyler
            if rtype==0:
                return StringIO(str(re.content, 'utf-8'))
            else:
                return re.text
        else:
            _log.error('Eror on dowloading intelligent http:' + str(re.status_code)+' [ '+getStackdata()+' ] ')

    except UnicodeDecodeError as e:
        _log.error('Eror parsing to string: '+ ' [ ' + getStackdata() + ' ] ')        #if parsing is fail,return orginal responce object
        return re
    except Exception as e:
        _log.error(repr(e))
        traceback.print_exc()
    return False



def loadfeeders():
    global _allfeeders_
    method_list = [func for func in dir(Feeders) if callable(getattr(Feeders, func)) and not func.startswith("__")]
    templist=[]
    for item in method_list:
        temp=getattr(Feeders,item)
        obje=temp().returnObject()
        if obje is None:
            continue
        templist.append([temp.u_interval,temp().returnObject()])
        obje.checkstatus()                      #todo if not available resource don't add list

    _allfeeders_=sorted(templist, key=lambda x: x[0])
    print(_allfeeders_)