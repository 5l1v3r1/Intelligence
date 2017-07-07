from constants.values import *
from  dbmanagment.dbmanagment import DbClient

_log=getlog()


def insertmanydb(self,dbname='intelligence',):
    client = DbClient()
    client.setdatabase('intelligence')
    for intel in self.intelligence:
        client.setcollection(getCollectName(self.getType(intel['collection'])))
        client.insertmany(intel['doc'])

