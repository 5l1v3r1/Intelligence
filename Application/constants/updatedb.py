
import pkgutil

import sys



from constants.values import Feeders
from constants.settings import ROOTPATH



_allfeeders_=[]

def loadfeeders():

    method_list = [func for func in dir(Feeders) if callable(getattr(Feeders, func)) and not func.startswith("__")]
    for item in method_list:
        temp=getattr(Feeders,item)
        obje=temp().returnObject()
        if obje is None:
            continue
        _allfeeders_.append([temp.u_interval,temp().returnObject()])
        print(obje.checkstatus())





print(ROOTPATH)


loadfeeders()
print(_allfeeders_)