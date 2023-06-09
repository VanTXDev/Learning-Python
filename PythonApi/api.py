from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort
from flask_pymongo import PyMongo
from bson.json_util import dumps

from database.UserDbMethodsNoSQL import UserDbMethodsNoSQL


app = Flask(__name__)
app.config["SECRET_KEY"] = "pythonapi20230609"
app.config["MONGO_URI"] = "mongodb+srv://vandev:<password>@cluster0.sjqwjeq.mongodb.net/NodeJSTutorial?retryWrites=true&w=majority"
#mongodb+srv://vandev:<password>@cluster0.sjqwjeq.mongodb.net/?retryWrites=true&w=majority
#mongodb+srv://vantx2103:<password>@cluster0.hhuncmh.mongodb.net/?retryWrites=true&w=majority

api = Api(app)
mongodb_client = PyMongo(app)
db = mongodb_client.db

user_login_args = reqparse.RequestParser()
user_login_args.add_argument("Username", type=str, help="username of user is required", required=True)
user_login_args.add_argument("Password", type=str, help="password of user is required", required=True)

class User(Resource):
    user_db_method = UserDbMethodsNoSQL(db)

    def get(self):
        try:
            result = self.user_db_method.get()
            return result
        except Exception as e:
            print(e)
            return None
        
    def post(self):
        args = user_login_args.parse_args();
        try:
            result = self.user_db_method.login(username=args['Username'], password=args['Password'])
            if not result:
                abort(404, message='No password or username match found')
            return result, 200
        except Exception as e:
            return abort(400, message="Login failed")


# @app.route('/users')
# def index():
#     users = db.users.find({"name": "John"}, {"name": 1, "email": 1, "_id": 0, "phoneNumber": 1})
#     results = dumps(users)
#     print (results)
#     return results, 200

api.add_resource(User, "/users/")

if __name__ == '__main__':
    app.run(debug=True)