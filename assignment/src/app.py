import os.path,json
from flask_cors import CORS
from flask import Flask,request,jsonify
from models import category_model,db_model,knowledge_model

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app)

dbModel = db_model.DbModel()
categoryModel = category_model.CategoryModel()
knowledgeModel = knowledge_model.KnowledgeModel()

@app.route('/user/',methods=['GET'])
def get_user_details():
    # This is the method used to view the users
    username,password = request.headers['Username'],request.headers['Password']
    if username == 'admin' and password == 'admin': return {'response':dbModel.find(),'status':200}
    else: return {'response':"You don't have permissions to view users",'status':500}

@app.route('/knowledge/',methods=['GET'])
def get_knowledge_details():
    # This is the method used to view the knowledge base
    username = request.headers['Username']
    obj = dbModel.find_by_record(username)
    if obj:
        if obj['role_name'] == 'author': return {'response':knowledgeModel.find(),'status':200}
        else: return {'response':"You don't have permissions to view knowledge base",'status':500}
    else: return {'response':"No Such User",'status':500}

@app.route('/user/',methods=['POST'])
def add_user():
    # This is the method to create an user
    if request.method == 'POST':
        if request.json:
            username,password = request.headers['Username'],request.headers['Password']
            if username == 'admin' and password == 'admin':
                if 'name' in request.json and 'role_name' in request.json and 'permissions' in request.json:
                    name = request.json['name']
                    role_name = request.json['role_name']
                    permissions = request.json['permissions']
                    response = dbModel.create({'name':name,'role_name':role_name,'permissions':permissions})
                    return {'response':response,'status':200}
                else: return {'response':"Some of the mandatory fields were missing",'status':500}
            else: return {'response':"You don't have permissions to create a user",'status':500}
        else: return {'response':"Send the request in Proper JSON Format.",'status':500}

@app.route('/knowledge/',methods=['POST'])
def add_knowledge():
    # This is the method to create a knowledge
    if request.method == 'POST':
        if request.json:
            username = request.headers['Username']
            print(username)
            obj = dbModel.find_by_record(username)
            if obj:
                if obj['role_name'] == 'author':
                    if 'knowledge_id' in request.json and 'knowledge_name' in request.json and 'description' in request.json and 'categories' in request.json:
                        knowledge_id = request.json['knowledge_id']
                        knowledge_name = request.json['knowledge_name']
                        description = request.json['description']
                        categories = request.json['categories']
                        response = knowledgeModel.create({'knowledge_id':knowledge_id,'knowledge_name':knowledge_name,
                                                'description':description,'categories':categories})
                        return {'response':response,'status':200}
                    else: return {'response':"Some of the mandatory fields were missing",'status':500}
                else: return {'response':"You don't have permissions to create a user",'status':500}
            else: return {'response':"No such user",'status':500}
        else: return {'response':"Send the request in Proper JSON Format.",'status':500}

@app.route('/user/<string:name>/', methods=['GET'])
def get_user(name):
    # This is the method to view a specific user
    username,password = request.headers['Username'],request.headers['Password']
    if username == 'admin' and password == 'admin': return {'response':dbModel.find_by_record(name),'status':200}
    else: return {'response':"You don't have permissions to know about users",'status':500}

@app.route('/knowledge/<string:kname>/', methods=['GET'])
def get_knowledge(kname):
    # This is the method to view a specific knowledge
    username = request.headers['Username']
    obj = dbModel.find_by_record(username)
    if obj:
        if obj['role_name'] == 'author': return {'response':knowledgeModel.find_by_record(kname),'status':200}
        else: return {'response':"You don't have permissions to know about knowledge base",'status':500}
    else: return {'response':"No such user",'status':500}

@app.route('/user/<string:name>/',methods=['PUT'])
def update_user(name):
    # This is the method to update a user
    if request.method == 'PUT':
        username,password = request.headers['Username'],request.headers['Password']
        if username == 'admin' and password == 'admin':
            role_name,permissions = request.json['role_name'],request.json['permissions']
            response = dbModel.update(name,{'role_name':role_name,'permissions':permissions})
            return {'response':response,'status':200}
        else: return {'response':"You don't have permissions to update users",'status':500}

@app.route('/knowledge/<string:kname>/',methods=['PUT'])
def update_knowledge(kname):
    # This is the method to update a knowledge
    if request.method == 'PUT':
        username = request.headers['Username']
        obj = dbModel.find_by_record(username)
        if obj:
            if obj['role_name'] == 'author':
                categories = request.json['categories']
                description = request.json['description']
                response = knowledgeModel.update(kname,{'categories':categories,'description':description})
                return {'response':response,'status':200}
            else: return {'response':"You don't have permissions to update knowledge base",'status':500}
        else: return {'response':"No such user",'status':500}

@app.route('/user/<string:uname>/',methods=['DELETE'])
def delete_user(uname):
    # This is the method to delete a user
    if request.method == 'DELETE':
        username,password = request.headers['Username'],request.headers['Password']
        if username == 'admin' and password == 'admin':
            dbModel.delete(uname)
            return {'response':'Record Deleted','status':200}
        else: return {'response':"You don't have permissions to delete users",'status':500}

@app.route('/knowledge/<string:kname>/',methods=['DELETE'])
def delete_knowledge(kname):
    # This is the method to delete a knowledge
    if request.method == 'DELETE':
        username = request.headers['Username']
        obj = dbModel.find_by_record(username)
        if obj:
            if obj['role_name'] == 'author':
                knowledgeModel.delete(kname)
                return {'response':'Record Deleted','status':200}
            else: return {'response':"You don't have permissions to delete knowledge base",'status':500}
        else: return {'response':"No such user",'status':500}

@app.route('/content/',methods=['POST'])
def add_content():
    # This is the method to add the content
    if request.method == 'POST':
        if request.json:
            username = request.headers['Username']
            obj = dbModel.find_by_record(username)
            if obj:
                if obj['role_name'] == 'author':
                    if 'file_path' in request.json:
                        file_path = request.json['file_path']
                        if os.path.isfile(file_path):
                            with open(file_path) as file1:
                                data = json.load(file1)
                                response = categoryModel.create(data)
                                return {'response':response,'status':200}
                        else: return {'response':"File not Found",'status':500}
                    else: return {'response':"Some of the mandatory fields were missing",'status':500}
                else: return {'response':"You don't have permissions to create content",'status':500}
            else: return {'response':"No such user",'status':500}
        else: return {'response':"Send the request in Proper JSON Format.",'status':500}

@app.route('/content/',methods=['GET'])
def get_content_details():
    # This is the method to view all the content
    username = request.headers['Username']
    obj = dbModel.find_by_record(username)
    if obj:
        if obj['role_name'] in ['reviewer','analyst','customer','all']:
            return {'response':categoryModel.find(),'status':200}
        else: return {'response':"You don't have permissions to view content base",'status':500}
    else: return {'response':"No such user",'status':500}

@app.route('/content_search/',methods=['POST'])
def search_content():
    # This is the method to search the content
    if request.method == 'POST':
        if request.json:
            username = request.headers['Username']
            obj = dbModel.find_by_record(username)
            if obj:
                if obj['role_name'] == 'customer':
                    if 'doc_type' in request.json and 'knowledge_name' in request.json and 'category' in request.json and 'query' in request.json:
                        doc_type = request.json['doc_type']
                        knowledge_name = request.json['knowledge_name']
                        category = request.json['category']
                        query = request.json['query']
                        result = categoryModel.search({'knowledge_name':knowledge_name,'category':category,
                                        'doc_type':doc_type,'query':query})
                        return {'No. of Results':len(result),'response':result,'status':200}
                    else: return {'response':"Some of the mandatory fields were missing",'status':500}
                else: return {'response':"You don't have permissions to search content base",'status':500}
            else: return {'response':"No such user",'status':500}
        else: return {'response':"Send the request in Proper JSON Format.",'status':500}

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port='7001')
