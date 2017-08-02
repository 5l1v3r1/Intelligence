"""
    MongoDb database managment, it serves for crud operation on database
    In addition information about collection and database
    'mongodb://arquanum:qPuDqX2e@138.68.92.9:27017/admin'
    mongo -u arquanum  138.68.92.9/admin -p qPuDqX2e
"""

import pymongo as mongo
from constants.values import  getlog
from constants.settings import  DBPATH
from core.common import getStackdata
from pymongo.errors import BulkWriteError

class DbClient(object):

    def __init__(self, database=None, collection=None):
        self.log = getlog()
        self.database = database
        self.collection = collection
        self.collectiondb = None
        self.client = None
        self.conectdb()

    def conectdb(self):
        try:
            self.client = mongo.MongoClient(DBPATH)
            info = self.client.server_info()
            self.log.info("Connected MongoDB "+ '[ '+getStackdata()+' ] ')
            return True
        except mongo.errors.ServerSelectionTimeoutError as err:
            self.log.error(repr(err))
            return False
        except Exception as err:
            self.log.error(repr(err))
            return False

    def check_field(self):
        if self.database == None or self.database == None:
            self.log.error("please choose databasename or collection,by calling setdatabase orsetcollection ")
            return False
        return True

    def set_database(self, database):
        self.database = database

    def set_collection(self, collection):
        self.collection = collection

    def collections(self):
        if self.check_field() == False: return
        database = self.client[self.database]
        collection = database.collection_names(include_system_collections=False)
        return collection

    def databases(self):
        return self.client.database_names()

    def check_being(self,filter):
        collection = self.get_collection()
        return collection.find(filter).count()

    def get_documents(self, filter={'_id':0}):
        collection = self.get_collection()
        return collection.find(filter)

    def get_collection(self):
        if self.check_field() == False: return
        database = self.client[self.database]
        collection = database[self.collection]
        return collection

    def insert(self, item):
        try:
            collection = self.get_collection()
            res = collection.insert_one(item)
            self.log.info("Inserted Succesfully: %d "%str(res.inserted_id)+'[ '+getStackdata()+' ] ')
        except mongo.errors.DuplicateKeyError as  exp:
            self.log.error(repr(exp))
            self.update(item)
        except Exception as  exp:
            self.log.error(repr(exp))

    def insert_many(self, items,flag=True):
        try:
            collection = self.get_collection()
            self.collectiondb = collection
            res = collection.insert_many(items, False)
            self.log.info("Inserted Succesfully %d items from "%len(res.inserted_ids)+'[ '+getStackdata()+' ] ')
        except BulkWriteError as bwe:
            werrors = bwe.details['writeErrors']
            updatelist = []
            for err_item in werrors:
                if err_item['code'] == 11000:
                    updatelist.append(items[err_item['index']])
            self.log.info("Inserted Succesfully %d items " %(len(items)-len(updatelist))+ "and "+str(len(updatelist))+" number items duplicated,so trying update  theses "+'[ '+getStackdata()+' ] ')
            #self.update_many(updatelist,flag)
        except Exception as  e:
            self.log.error(repr(e))

    def update_many(self, items,flag=True):
        for item in items:
            self.update(item,flag)

    def delete(self, parameter={'name': 'fatih'}):
        try:
            collection = self.get_collection()
            output = collection.delete_one(parameter)
            if output.deleted_count != 0:
                self.log.info("Deleted Succesfully: ")
            else:
                self.log.info("Unsuccesfully on deleted : " + str(output.raw_result))
        except Exception as  e:
            self.log.error(repr(e))

    def update(self, item,flag=True):
        check = None
        try:
            check = self.check_last_intelligence(item)
            #print(set(check))
            if (check == False or check == None) and flag:
                result = self.collectiondb.update(
                    {"_id": item['_id']},
                    {
                        "$addToSet": {"Intelligence": {"$each": item['Intelligence']}},
                        "$set": {
                            "lastDate": item['lastDate'],
                            "type": item['type'],  # c&c
                            "description": item['description'],
                            "by": item['by']
                        }
                    }
                )
            else:
                result = self.collectiondb.update(
                    {"_id": item['_id']},
                    {

                        "$set": {
                            "lastDate": item['lastDate'],
                            "type": item['type'],  # c&c
                            "description": item['description'],
                            "by": item['by'],
                            "Intelligence":check
                        }
                    }
                )

            #print(result)

        except Exception as  e:
            self.log.error(repr(e))

    def check_last_intelligence(self, item):
        result = self.collectiondb.find_one({"_id": item['_id']})
        index = 0
        intelligence = result['Intelligence']
        while index < len(intelligence):

            if intelligence[index]['by'] == item['by']:
                datechunk = intelligence[index]['datechunk']
                datechunk.insert(0, item['lastDate'])
                intelligence[index]['datechunk'] = list(set(datechunk))
                return intelligence
            index += 1

        return False