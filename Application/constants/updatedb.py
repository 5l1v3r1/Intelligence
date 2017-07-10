
import pkgutil

import sys
from .values import Feeders
from .settings import *




def loadfeeders():

    method_list = [func for func in dir(Feeders) if callable(getattr(Feeders, func)) and not func.startswith("__")]
    allfeeds=[]
    for item in method_list:
        feed=getattr(Feeders,item)
        feedobje=feed().returnObject()
        if feedobje is None:
            continue
        allfeeds.append([feed.u_interval,feed().returnObject()])
        print(feedobje.checkstatus())
        print(allfeeds)



__all__ = []


print(ROOTPATH)



loadfeeders()