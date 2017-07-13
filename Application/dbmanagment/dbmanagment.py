import pymongo as mongo
from constants.values import  *
from constants.settings import  DBPATH
import traceback
from pymongo.errors import BulkWriteError

description = """
    MongoDb database managment
    it serves for crud operation on database
    In addition information about collection and database
    'mongodb://arquanum:qPuDqX2e@138.68.92.9:27017/admin'
    mongo -u arquanum  138.68.92.9/admin -p secret
"""



class DbClient(object):

    def __init__(self,database=None,collection=None,ip='127.0.0.1',port='27017'):
        self.log=getlog()
        self.ip = ip
        self.database=database
        self.collection=collection
        self.port = port
        self.client=None
        self.conectdb()

    def conectdb(self):
        try:
            self.client = mongo.MongoClient(DBPATH)
            info=self.client.server_info()
            self.log.info("Connected MongoDB ")
            return True
        except  mongo.errors.ServerSelectionTimeoutError as err:
            self.log.error(repr(err))
            return False
        except  Exception as err:
            self.log.error(repr(err))
            return False



    def checkField(self):
        if (self.database == None or self.database == None):
            self.log.error("please choose databasename or collection,by calling setdatabase orsetcollection ")
            return False
        return True


    def collections(self):
        if self.checkField()==False:return
        database = self.client[self.database]
        collection = database.collection_names(include_system_collections=False)
        return collection


    def databases(self):
        return self.client.database_names()

    def setdatabase(self,database):
        self.database=database

    def setcollection(self, collection):
        self.collection = collection

    def getdocuments(self,filter={}):
        collection = self.getCollection()
        cursor=collection.find(filter)
        for document in cursor:
           print(document)
        return cursor

    def getCollection(self):
        if self.checkField() == False: return
        database = self.client[self.database]
        collection = database[self.collection]
        return collection



    def insert(self,item):
        try:
            collection=self.getCollection()
            r=collection.insert_one(item)

            self.log.info("Inserted Succesfully:"+str(r.inserted_id))
        except mongo.errors.DuplicateKeyError as  e:
            self.log.error(repr(e))
            self.update(item)
        except Exception as  e:
            self.log.error(repr(e))

    def insertmany(self, items):
        try:
            collection = self.getCollection()
            r = collection.insert_many(items,False)
            self.log.info("Inserted Succesfully %d items"%len(r.inserted_ids))
        except BulkWriteError as bwe:
            werrors = bwe.details['writeErrors']
            updatelist=[]
            for err_item in werrors:
                if err_item['code']==11000:
                    updatelist.append(items[err_item['index']])
            self.log.info(str(len(updatelist))+" number items duplicated,so trying update  theses")
            self.updatemany(updatelist)
        except Exception as  e:
            self.log.error(repr(e))

    def updatemany(self,items):
        for item in items:
            self.update(item)

    def delete(self,id):
        try:
            collection = self.getCollection()
            output=collection.delete_one({'name': 'fatih'})
            if output.deleted_count!=0:
                self.log.info("Deleted Succesfully: ")
            else:
                self.log.info("Unsuccesfully on deleted : " + str(output.raw_result))
        except Exception as  e:
            self.log.error(repr(e))

    def update(self,item):
        try:
            collection = self.getCollection()
            result=collection.update(
                  { "_id": item['_id'] },
             {
                  "$addToSet": { "Intelligence": { "$each": item['Intelligence'] } },
                    "$set": {
                        "lastDate": item['lastDate'],
                        "type": item['type'],  # c&c
                        "description": item['description'],
                        "by": item['by'],
                         }
             }
            );
            #print(result)

        except Exception as  e:
            self.log.error(repr(e))


"""

def getItemDictionary(items):
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
    return listdict

items=[['188.248.147.235','2017-06-23 01:10:35.063',"Incoming Masscan detected"],
       ['1.246.101.246','2017-06-23 01:08:44.433',"RA SCAN Unusually fast Terminal Server Traffic Inbound"],
        ['5.8.48.21','2017-06-23 01:08:44.922',"MS Terminal Server scanner taffic on Non-standard Port"]
       ]

client=DbClient(ip='138.68.92.9')
print(client.databases())
client.setdatabase('intelligence')
print(client.collections())
client.setcollection('ip')
#client.getdocuments()
#client.delete('594a740fde163924ae0cd1d9')
client.insertmany(getItemDictionary(items))




client.insert(
                {
                    "_id":1,
                    "lastDate": 2,
                    "type":"BlackIP",
                    "description": 3,
                    "by": self.by,
                    "Intelligence":
                    [{
                         "lastDate":  item[1],
                         "type": "BlackIP",
                         "description": item[2],
                         "by": self.by,
                         "confidence": "alahaemanet"
                    }]
                }
            )


"""
