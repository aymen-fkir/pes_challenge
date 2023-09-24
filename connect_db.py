from pymongo import MongoClient


client = MongoClient(host="localhost",port=27017)

db = client["Energy"]
collection = db["users"]
re = collection.find_one({"_id":{"$oid":"650f20af038c13f1c99c9615"}})

print(re)
client.close()