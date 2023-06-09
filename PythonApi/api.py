from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = "pythonapi20230609"
app.config["MONGO_URI"] = "mongodb+srv://vandev:admin123@cluster0.sjqwjeq.mongodb.net/NodeJSTutorial?retryWrites=true&w=majority"
#mongodb+srv://vandev:<password>@cluster0.sjqwjeq.mongodb.net/?retryWrites=true&w=majority
#mongodb+srv://vantx2103:<password>@cluster0.hhuncmh.mongodb.net/?retryWrites=true&w=majority

api = Api(app)
mongodb_client = PyMongo(app)
db = mongodb_client.db

@app.route('/')
def index():
    users = db.users.find_one({"name": "John"})
    users["_id"] = "1"
    users = jsonify(users)
    print (users)
    return users, 200

if __name__ == '__main__':
    app.run(debug=True)