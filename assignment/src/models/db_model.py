from factory import database

class DbModel(object):
    def __init__(self):
        self.db = database.Database()
        self.collection = 'genesys_users'
        self.fields = {
            "name": "string",
            "created_time": "datetime",
            "updated_time": "datetime",
            "role_name": "string",
            "permissions": "string"
        }
    
    def create(self,db_object):
        res = self.db.insert(db_object,self.collection,'name')
        if res: return "Record Inserted Successfully"
        else: return "Record Insertion Failed"

    def find(self):
        return self.db.find(self.collection)

    def find_by_role(self,role):
        return self.db.find_by_role(role,self.collection)

    def find_by_record(self,name):
        return self.db.find_by_record(name,self.collection,'name')

    def update(self,name,data_obj):
        return self.db.update(name,data_obj,self.collection,'name')
    
    def delete(self,name):
        return self.db.delete(name,self.collection,'name')
