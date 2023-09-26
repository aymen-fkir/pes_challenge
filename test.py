from pymongo import MongoClient


def check_admin(data):
    client = MongoClient(host="localhost",port=27017)
    db = client["Energy"]
    collection = db["admins"]
    result = collection.find_one(data)
    if result == None:
        return 401
    else:
        return result
re = check_admin({"username":"hama","password":"147"})
print(type(re))