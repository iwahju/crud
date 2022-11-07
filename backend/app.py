from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask_cors import CORS


app = Flask(__name__)
cors = CORS(app)

client = MongoClient(
    "mongodb+srv://andrewg3:Sshdwrnd1@cluster0.sx6hgc8.mongodb.net/test?retryWrites=true&w=majority"
)

db = client["test"]  ## database name


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/user/", methods=["POST", "GET"])
def data():

    # POST a data to database
    if request.method == "POST":
        body = request.json
        name = body["name"]
        password = body["password"]
        email = body["email"]
        inventory = body["inventory"]
        shoppingList = body["shoppingList"]
        # db.users.insert_one({
        db["user-data"].insert_one(
            {
                "name": name,
                "password": password,
                "email": email,
                "inventory": inventory,
                "shoppingList": shoppingList,
            }
        )
        return jsonify(
            {
                "status": "Data is posted to MongoDB!",
                "name": name,
                "password": password,
                "email": email,
                "inventory": inventory,
                "shoppingList": shoppingList,
            }
        )

        # GET all data from database
    if request.method == "GET":
        allData = db["user-data"].find()
        dataJson = []
        for data in allData:
            id = data["_id"]
            name = data["name"]
            password = data["password"]
            email = data["email"]
            inventory = data["inventory"]
            shoppingList = data["shoppingList"]

            dataDict = {
                "id": str(id),
                "name": name,
                "password": password,
                "email": email,
                "inventory": inventory,
                "shoppingList": shoppingList,
            }
            dataJson.append(dataDict)
        print(dataJson)
        return jsonify(dataJson)


@app.route("/user/<string:id>", methods=["GET", "DELETE", "PUT"])
def onedata(id):

    # GET a specific data by id
    if request.method == "GET":
        data = db["user-data"].find_one({"_id": ObjectId(id)})
        id = data["_id"]
        name = data["name"]
        password = data["password"]
        email = data["email"]
        inventory = data["inventory"]
        shoppingList = data["shoppingList"]
        dataDict = {
            "id": str(id),
            "name": name,
            "password": password,
            "email": email,
            "inventory": inventory,
            "shoppingList": shoppingList,
        }
        print(dataDict)
        return jsonify(dataDict)

    if request.method == "PUT":
        body = request.json
        name = body["name"]
        password = body["password"]
        email = body["email"]
        inventory = body["inventory"]
        shoppingList = body["shoppingList"]

        db["user-data"].update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "name": name,
                    "password": password,
                    "email": email,
                    "inventory": inventory,
                    "shoppingList": shoppingList,
                }
            },
        )

        print("\n # Update successful # \n")
        return jsonify({"status": "Data id: " + id + " is updated!"})

    if request.method == "DELETE":
        db["users"].delete_many({"_id": ObjectId(id)})
        print("\n # Deletion successful # \n")
        return jsonify({"status": "Data id: " + id + " is deleted!"})


if __name__ == "__main__":
    app.debug = True
    app.run()
