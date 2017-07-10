import requests
import traceback
import constants.values as C
from constants.settings import *
from io import StringIO


_log=C.getlog()

def checkstatus(url):
    try:
        return url_ok(url)  # link is available
    except Exception as e:
        _log.error(repr(e))
        return False


def url_ok( url):
    r = requests.head(url,headers=HEADERS,timeout=TIMEOUT)
    return r.status_code == 200


def getPage(url,parameter=None):

    try:
        _log.info("Trying  to  connect page ")
        r = requests.get(url,headers=HEADERS,timeout=TIMEOUT)
        if r.status_code == 200:
            _log.info("Page retrieved")
            return StringIO(str(r.content, 'utf-8'))
        else:
            _log.error('Eror on dowloading intelligent http:' + str(r.status_code))

    except Exception as e:
        _log.error(repr(e))
        traceback.print_exc()
    return False



