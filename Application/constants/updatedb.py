try:
    import constants.settings
except:
    import settings
import core.common as common
import threading
from datetime import datetime

_log_=common.getlog()
_threadlist_=[]



class FeederThread(threading.Thread):
    def __init__(self, id, feed):
        threading.Thread.__init__(self)
        self.name = feed.name
        self.threadID = id
        self.obje = feed

    def run(self):
        _log_.info("Thread started:"+self.obje.name)
        print(self.obje.checkstatus)
        self.obje.getIntelligent()
        self.obje.insertdb()
        _log_.info("Thred exited:" + self.obje.name)






_log_.info("Started thread feeders")
start = datetime.now()
if len(common._allfeeders_ ) ==0:
    common.loadfeeders()
print(common._allfeeders_)
counter=0

for item in common._allfeeders_:
    thread = FeederThread(counter,item[1])
    thread.start()
    _threadlist_.append(thread)
    counter+=1



print(_threadlist_)

for x in _threadlist_:
    x.join()
end = datetime.now()

_log_.info("Finish thread feeders")
print("Total Time ",end-start)

