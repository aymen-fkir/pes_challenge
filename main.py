from flask import Flask ,render_template,request

from pymongo import MongoClient
import hashlib





def fetch_by_username(username):
    client = MongoClient(host="localhost",port=27017)
    db = client["Energy"]
    collection = db["users"]
    user = collection.find_one(username)
    client.close()
    return user

def check_username_unique(username):
    client = MongoClient(host="localhost",port=27017)
    db = client["Energy"]
    collection = db["users"]
    data = collection.find({"username":username})
    client.close()
    return data.count()

def insert_to_db(data):
    client = MongoClient(host="localhost",port=27017)

    db = client["Energy"]
    collection = db["users"]
    try:
        collection.insert_one(data)
        code = 200
    except:
        code = 121
    client.close()
    return code

def check_admin(data):
    client = MongoClient(host="localhost",port=27017)
    db = client["Energy"]
    collection = db["admins"]
    result = collection.find_one(data)
    if result == None:
        return 401
    else:
        return result

def fetch_db(data):
    sha256 = hashlib.sha256()
    client = MongoClient(host="localhost",port=27017)
    db = client["Energy"]
    collection = db["users"]
    sha256.update(data["password"].encode('utf-8'))
    data["password"] = sha256.hexdigest()
    result = collection.find_one(data)
    if result == None:
        return 401
    else:
        return result
    

app = Flask(__name__)
# main route
@app.route("/")
def home():
    return render_template("index.html")

#for signout
@app.route('/signout')
def signout():
    return app.redirect(app.url_for('home'))

#for signin
@app.route("/signin",methods=["POST"])
def signin():
    data = {"username":request.form["username"],"password":request.form["password"]}
    
    re = check_admin(data)
    if re == 401:
        result = fetch_db(data)
        if result == 401:
            return app.redirect(f"/")
        
        return app.redirect(f"/profile/{result['username']}")
    return app.redirect(f"/admin/{re['region']}/{data}")

#for adminrout
@app.route("/admin/<region>/<username>")
def admin(region,username):
    client = MongoClient(host="localhost",port=27017)
    db = client["Energy"]
    collection = db["users"]
    user_data = collection.find({"region":region})
    return render_template("adminpage.html",user_data=user_data)

#for signup
@app.route("/signup")
def signup():
    return render_template("signup.html")

#for creating account
@app.route("/create_account",methods=['POST'])
def create_account():
    sha256 = hashlib.sha256()
    form = request.form
    sha256 = hashlib.sha256()
    if form["ver_password"] == form["password"]:
        sha256.update(form["password"].encode('utf-8'))
        hashed_data = sha256.hexdigest()

        data = {"username":form["username"],"email":form["email"],"password":hashed_data,"energy_consumtion":0,"cost":0,"polution":0,"region":"east cost"}
        verification_user = check_username_unique(data["username"])
        if verification_user!=0:
            return app.redirect("/signup")
        
        code = insert_to_db(data)
        if code == 200:
            return app.redirect("/")
    return app.redirect("/signup")

# for user page


@app.route("/profile/<username>")
def userinerface(username):
    profile = fetch_by_username({"username":username})
    return render_template("userpage.html",profile=profile)

if __name__ == "__main__":
    app.run(debug=True)