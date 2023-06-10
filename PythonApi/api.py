from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort
from flask_pymongo import PyMongo
from bson.json_util import dumps

from database.UserDbMethodsNoSQL import UserDbMethodsNoSQL
from models.User import UserModel


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

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("Name", type=str, help="Name of user is required", required=True)
user_put_args.add_argument("Email", type=str, help="Email of user is required", required=True)
user_put_args.add_argument("Username", type=str, help="Username of user is required", required=True)
user_put_args.add_argument("Password", type=str, help="password of user is required", required=True)
user_put_args.add_argument("PhoneNumber", type=str, help="PhoneNumber of user is required", required=True)
user_put_args.add_argument("Address", type=int, help="Address of user is required", required=True)

def handle_error(err):
    return f"{err.__class__.__name__}: {err}"

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
        args = user_login_args.parse_args()
        try:
            result = self.user_db_method.login(username=args['Username'], password=args['Password'])
            if result is None:
                return abort(404, message='No password or username match found')
            return jsonify(result)
        except Exception as e:
            return handle_error(e)
            # return abort(400, message="Login failed")

    def put(self):
        args = user_put_args.parse_args()
        try:
            userExist = self.user_db_method.get_user_by_name(name=args['Name'])
            if userExist:
                return abort(400, message="User already exists")

            userObj = UserModel(name=args['Name'], email=args['Email'], username=args['Username'], password=args['Password'], phoneNumber=args['PhoneNumber'], address=args['Address'])
            user = self.user_db_method.put(userObj)
            if user is None:
                return abort(409, message="Couldn't create user")
            return user
        except Exception as e:
            return handle_error(e)

api.add_resource(User, "/users/")

if __name__ == '__main__':
    app.run(debug=True)