from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from config import config
import re

class Database(object):
    def __init__(self):
        self.client = MongoClient(config['db']['url'])
        self.db = self.client[config['db']['name']]
    
    def insert(self,db_object,collection,field_name):
        db_object['created_time'],db_object['updated_time'] = datetime.now(),datetime.now()
        insert_obj = self.db[collection].update_one({field_name:re.compile(db_object[field_name],re.IGNORECASE)},{'$set':db_object},upsert = True)
        return insert_obj.acknowledged

    def insert_many(self,db_object,collection):
        data = []
        for obj in db_object:
            obj['created_time'],obj['updated_time'] = datetime.now(),datetime.now()
            data.append(obj)
        insert_obj = self.db[collection].insert_many(data)
        return insert_obj.acknowledged
    
    def find(self,collection):
        cursor,records = self.db[collection].find(),[]
        if cursor:
            for obj in cursor:
                del obj['_id']
                records.append(obj)
        cursor.close()
        return records

    def find_by_role(self,role,collection):
        cursor,records = self.db[collection].find({'role_name':re.compile(role,re.IGNORECASE)}),[]
        if cursor:
            for obj in cursor:
                del obj['_id']
                records.append(obj)
        cursor.close()
        return records

    def find_by_record(self,record,collection,field_name):
        obj = self.db[collection].find_one({field_name:re.compile(record,re.IGNORECASE)})
        if obj: 
            del obj['_id']
            return obj
        return None

    def update(self,username,data_obj,collection,field_name):
        data_obj['updated_time'] = datetime.now()
        update_obj = self.db[collection].update_one({field_name:re.compile(username,re.IGNORECASE)},{'$set':data_obj})
        if update_obj.matched_count == 1: return 'Record Successfully Updated'
        else: return 'Record Updation Failed'
    
    def delete(self,username,collection,field_name):
        delete_obj = self.db[collection].delete_one({field_name:re.compile(username,re.IGNORECASE)})
        return bool(delete_obj.deleted_count)

    def search(self,query_object,collection):
        query,records = query_object['query'].split(),[]
        regex_query = [re.compile(qry,re.IGNORECASE) for qry in query]
        search_field = 'question' if query_object['doc_type'].lower() == 'faq' else 'title'
        cursor = self.db[collection].find({'$and':[{'knowledge_name':re.compile(query_object['knowledge_name'],re.IGNORECASE)},
                            {'category':re.compile(query_object['category'],re.IGNORECASE)},{'doc_type':re.compile(query_object['doc_type'],re.IGNORECASE)},
                            {search_field:{'$in':regex_query}}]})

        if cursor:
            for obj in cursor:
                del obj['_id']
                records.append(obj)
        
        cursor.close()
        return records