import asyncio
import graphene
from starlette.applications import Starlette
from starlette_graphene3 import GraphQLApp, make_graphiql_handler
from datetime import datetime


class Dates(graphene.ObjectType):
    lastlogin = graphene.DateTime()
    register = graphene.DateTime()


class User(graphene.ObjectType):
    name = graphene.String()
    surname = graphene.String()
    dates = graphene.Field(lambda: Dates)

    def resolve_dates(root, info):
        return {"lastlogin": datetime.now(), "register": datetime.now()}


class Query(graphene.ObjectType):
    me = graphene.Field(User, name=graphene.String(), surname=graphene.String())

    def resolve_me(root, info, name=None, surname=None):
        return {"name": name, "surname": surname}

app = Starlette()
schema = graphene.Schema(query=Query)

app.mount("/main", GraphQLApp(schema, on_get=make_graphiql_handler()))  # Graphiql IDE

# app.mount("/", GraphQLApp(schema, on_get=make_playground_handler()))  # Playground IDE
# app.mount("/", GraphQLApp(schema)) # no IDE


# import asyncio
# import graphene
# from starlette.applications import Starlette
# from starlette_graphene3 import GraphQLApp, make_graphiql_handler
# from datetime import datetime
# from pymongo import MongoClient


# class Dates(graphene.ObjectType):
#     lastlogin = graphene.DateTime()
#     register = graphene.DateTime()


# class User(graphene.ObjectType):
#     name = graphene.String()
#     surname = graphene.String()
#     dates = graphene.Field(lambda: Dates)

#     def resolve_dates(root, info):
#         return {"lastlogin": datetime.now(), "register": datetime.now()}


# class Query(graphene.ObjectType):
#     me = graphene.Field(User, name=graphene.String(), surname=graphene.String())

#     def resolve_me(root, info, name=None, surname=None):
#         # Initialize the MongoDB client
#         client = MongoClient("mongodb://localhost:27017/")
#         db = client["mydatabase"]  # Replace "mydatabase" with the name of your database
#         collection = db["users"]  # Replace "users" with the name of your collection

#         # Create a document to insert to the collection
#         user = {"name": name, "surname": surname, "dates": {"lastlogin": datetime.now(), "register": datetime.now()}}
#         # Insert the document to the collection
#         collection.insert_one(user)

#         # Return the user as a graphene object
#         return User(name=name, surname=surname)

# app = Starlette()
# schema = graphene.Schema(query=Query)

# app.mount("/main", GraphQLApp(schema, on_get=make_graphiql_handler()))  # Graphiql IDE

# # app.mount("/", GraphQLApp(schema, on_get=make_playground_handler()))  # Playground IDE
# # app.mount("/", GraphQLApp(schema)) # no IDE
