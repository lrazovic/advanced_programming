from pymongo import MongoClient
import os

mongo_service_name = "mongodb"
if 'MONGODB_HOST' in os.environ:
    connection_string = f"mongodb://admin:password@{os.environ['MONGODB_HOST']}"
else:
    connection_string = f"mongodb://admin:password@{mongo_service_name}"
client = MongoClient(connection_string, 27017)
db = client["usersdata"]
