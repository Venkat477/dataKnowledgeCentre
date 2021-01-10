from factory import database

class KnowledgeModel(object):
    def __init__(self):
        self.db = database.Database()
        self.collection = 'genesys_knowledgeBase'
        self.fields = {
            "knowledge_id": "integer",
            "knowledge_name": "string",
            "description": "string",
            "created_time": "datetime",
            "updated_time": "datetime",
            "categories": "list"
        }
    
    def create(self,db_object):
        res = self.db.insert(db_object,self.collection,'knowledge_id')
        if res: return "Record Inserted Successfully"
        else: return "Record Insertion Failed"

    def find(self):
        return self.db.find(self.collection)

    def find_by_record(self,knowledge_name):
        return self.db.find_by_record(knowledge_name,self.collection,'knowledge_name')

    def update(self,username,data_obj):
        return self.db.update(username,data_obj,self.collection,'knowledge_name')
    
    def delete(self,username):
        return self.db.delete(username,self.collection,'knowledge_name')

