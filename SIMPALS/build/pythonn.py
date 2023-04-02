from pymongo import MongoClient
from fastapi import Form, FastAPI, Request
from fastapi.responses import HTMLResponse
from datetime import datetime
import os
app = FastAPI()

client = MongoClient("mongodb://mongodb:27017")
databases = client.list_database_names()

db = client["mydatabase"]

collection = db["mycollection"]

@app.get('/main')
async def gett():
    page_path = os.path.abspath(os.path.join(os.getcwd(),"FrontEnd/main_page.html"))
    with open(page_path) as f:
        page = f.read()
    return HTMLResponse(content=page)

@app.post('/main')
async def postt(name:str=Form(...),surname:str=Form(...)):
    new_doc = {
        "name": name,
        "surname": surname,
        "dates": {
            "lastlogin": str(datetime.utcnow()),
            "register": str(datetime.utcnow())
        }
    }

    result = collection.insert_one(new_doc)
    print(result.inserted_id)
    print(name, surname)
    page_path = os.path.abspath(os.path.join(os.getcwd(),"FrontEnd/main_page.html"))
    with open(page_path) as f:
        page = f.read()
    return HTMLResponse(content=page)

@app.get('/users')
async def get_users(request: Request):
    cursor = collection.find({})
    users = ''
    i = 0
    for document in cursor:
        i += 1
        last_login = document['dates']['lastlogin']
        register = document['dates']['register']
        users += f"<tr><td>{i}</td><td>{document['_id']}</td><td>{document['name']}</td><td>{document['surname']}</td><td>{last_login}</td><td>{register}</td><td><button class='delete-btn'>Delete</button></td></tr>"
    
    page_path = os.path.abspath(os.path.join(os.getcwd(),"FrontEnd/users.html"))
    with open(page_path) as f:
        page = f.read()
    base_data=page.replace("%s",f"{users}")
    return HTMLResponse(base_data)


# from fastapi import FastAPI
# from bson.objectid import ObjectId
# from pymongo import MongoClient
# from datetime import datetime
# import os

# app = FastAPI()

# client = MongoClient("mongodb://mongodb:27017")
# db = client["mydatabase"]
# collection = db["mycollection"]

# @app.get('/main')
# async def gett():
#     page_path = os.path.abspath(os.path.join(os.getcwd(),"FrontEnd/main_page.html"))
#     with open(page_path) as f:
#         page = f.read()
#     return HTMLResponse(content=page)

# @app.post('/graphql')
# async def graphql(request: Request):
#     data = await request.json()
#     query = data['query']
#     variables = data.get('variables')
#     result = await execute(query, variables)
#     return JSONResponse(result)

# async def execute(query, variables):
#     if variables is None:
#         variables = {}
#     schema = build_schema()
#     return await graphql(schema, query, variables=variables)

# def build_schema():
#     query_type = create_query_type()
#     mutation_type = create_mutation_type()
#     types = [query_type, mutation_type, UserType, UserDatesType]
#     schema = GraphQLSchema(query=query_type, mutation=mutation_type, types=types)
#     return schema

# def create_query_type():
#     query_fields = {
#         'databases': Field(List(String), resolve=get_databases)
#     }
#     return ObjectType('Query', fields=query_fields)

# def create_mutation_type():
#     mutation_fields = {
#         'createUser': Field(NonNull(ID), args={
#             'name': Argument(NonNull(String)),
#             'surname': Argument(NonNull(String))
#         }, resolve=create_user)
#     }
#     return ObjectType('Mutation', fields=mutation_fields)

# async def get_databases():
#     client = MongoClient("mongodb://mongodb:27017")
#     databases = client.list_database_names()
#     return databases

# async def create_user(root, info, name, surname):
#     new_doc = {
#         "name": name,
#         "surname": surname,
#         "dates": {
#             "lastlogin": str(datetime.utcnow()),
#             "register": str(datetime.utcnow())
#         }
#     }
#     result = collection.insert_one(new_doc)
#     return str(result.inserted_id)

# UserType = ObjectType('User', {
#     'name': Field(NonNull(String)),
#     'surname': Field(NonNull(String)),
#     'dates': Field(NonNull(UserDatesType))
# })

# UserDatesType = ObjectType('UserDates', {
#     'lastlogin': Field(NonNull(String)),
#     'register': Field(NonNull(String))
# })

