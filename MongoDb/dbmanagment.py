import pymongo as mongo
import logging
import datetime


description = """
    MongoDb database managment
    it serves for crud operation on database
    In addition information about collection and database
"""



class DbClient(object):

    def __init__(self,database=None,collection=None,ip='127.0.0.1',port='27017'):
        self.log=self.getlog()
        self.ip = ip
        self.database=database
        self.collection=collection
        self.port = port
        try:
            self.client = mongo.MongoClient(ip +':'+ port)
            info=self.client.server_info()
            self.log.info("Connected MongoDB ")
        except  mongo.errors.ServerSelectionTimeoutError as err:
            self.log.error(repr(err))


    def getlog(self):
        logFormatter = logging.Formatter("%(asctime)s [%(filename)s  %(funcName)s %(lineno)s] [%(levelname)-5.5s]  %(message)s")
        rootLogger = logging.getLogger()

        if (len(rootLogger.handlers)>0):
            return rootLogger
        rootLogger.setLevel(logging.INFO)
        fileHandler = logging.FileHandler('logfile.log')
        fileHandler.setFormatter(logFormatter)
        rootLogger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        rootLogger.addHandler(consoleHandler)

        return rootLogger


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
       #for document in cursor:
       #    print(document)
        return cursor



    def getCollection(self):
        if self.checkField() == False: return
        database = self.client[self.database]
        collection = database[self.collection]
        return collection



    def insert(self,item):

        try:
            collection=self.getCollection()
            output=collection.insert_one(item)
            self.log.info("Inserted Succesfully: "+output)
        except mongo.errors.DuplicateKeyError as  e:
            self.log.error(repr(e))
            self.update(item)
        except Exception as  e:
            self.log.error(repr(e))



    def update(self,item):
        try:
            collection = self.getCollection()
            collection.update(
                  { "_id": item['_id'] },
             {
                  "$addToSet": { "Intelligence": { "$each": item['Intelligence'] } },
                    "$set": {
                        "lastDate": datetime.datetime.utcnow(),
                        "type": item['type'],  # c&c
                        "description": item['description'],
                        "by": item['by'],
                         }
             }
            );

        except Exception as  e:
            self.log.error(repr(e))




client=DbClient()
print(client.databases())
client.setdatabase('EmployeeData')
print(client.collections())
client.setcollection('Employees')
print(client.getdocuments())


client.insert({
                "_id": '192.168.2.25',
                "lastDate": datetime.datetime.utcnow(),
                "type": 'aaaa',#c&c
                "description": "bbbb",
                "by":'Konya',
                "Intelligence":[{
                    "lastDate": datetime.datetime.utcnow(),
                    "type": 'aaaa',  # c&c
                    "description": "bbbb",
                    "by": "Konya",
                    "sepep":"Sanane tirt",
                    "result":"alahuekber"
                }]
            })


