from factory import database

class CategoryModel(object):
    def __init__(self):
        self.db = database.Database()
        self.collection = 'genesys_categories'
        self.fields = {
            "knowledge_name": "string",
            "category": "string",
            "doc_type": "string",
            "question": "string",
            "answer": "string",
            "title": "string",
            "content": "string"
        }
    
    def create(self,db_object):
        res = self.db.insert_many(db_object,self.collection)
        if res: return "Record Inserted Successfully"
        else: return "Record Insertion Failed"

    def find(self):
        return self.db.find(self.collection)

    def search(self,query_object):
        return self.db.search(query_object,self.collection)
