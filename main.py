from flask import Flask ,render_template,request

from pymongo import MongoClient

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
    client = MongoClient(host="localhost",port=27017)
    db = client["Energy"]
    collection = db["users"]
    result = collection.find_one(data)
    if result == None:
        return 401
    else:
        return result
    

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("front_page.html")

@app.route('/signout')
def signout():
    return app.redirect(app.url_for('home'))

@app.route("/signin",methods=["POST"])
def signin():
    data = request.form
    
    re = check_admin(data)
    if re == 401:
        result = fetch_db(data)
        if result == 401:
            return app.redirect("/")
        else:
            return app.redirect(f"/profile/{result['username']}")
    else:
        return app.redirect(f"/admin/{re['region']}/{re['username']}")

@app.route("/admin/<region>/<username>")
def admin(region,username):
    client = MongoClient(host="localhost",port=27017)
    db = client["Energy"]
    collection = db["users"]
    user_data = collection.find({"region":region})
    return render_template("adminpage.html",user_data=user_data)

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/create_account",methods=['POST'])
def create_account():
    form = request.form
    if form["ver_password"] == form["password"]:
        data = {"username":form.get("username"),"email":form.get("email"),"password":form.get("password"),"energy_consumtion":0,"cost":0,"polution":0,"region":"east cost"}
        code = insert_to_db(data)
        if code == 200:
            return app.redirect("/")
    return app.redirect("/signup")

@app.route("/profile/<username>")
def userinerface(username):
    profile = fetch_db({"username":username})
    return render_template("userpage.html",profile=profile)

if __name__ == "__main__":
    app.run(debug=True)