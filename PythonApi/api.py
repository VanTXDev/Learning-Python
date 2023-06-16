from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort
from flask_pymongo import PyMongo
from bson.json_util import dumps
from dotenv import load_dotenv
import datetime
import os

from database.UserDbMethodsNoSQL import UserDbMethodsNoSQL
from database.ToDoDbMethodsNoSQL import ToDoDbMethodsNoSQL
from models.User import UserModel
from models.ToDo import ToDoModel

load_dotenv()  # take environment variables from .env.
app = Flask(__name__)
app.config["SECRET_KEY"] = "pythonapi20230609"
app.config["MONGO_URI"] = os.getenv("MONGODB_URI1")

api = Api(app)
mongodb_client = PyMongo(app)
db = mongodb_client.db

user_login_args = reqparse.RequestParser()
user_login_args.add_argument("Username", type=str, help="Username of user is required", required=True)
user_login_args.add_argument("Password", type=str, help="Password of user is required", required=True)

user_put_args = reqparse.RequestParser()
user_put_args.add_argument("Name", type=str, help="Name of user is required", required=True)
user_put_args.add_argument("Email", type=str, help="Email of user is required", required=True)
user_put_args.add_argument("Username", type=str, help="Username of user is required", required=True)
user_put_args.add_argument("Password", type=str, help="password of user is required", required=True)
user_put_args.add_argument("PhoneNumber", type=str, help="PhoneNumber of user is required", required=True)
user_put_args.add_argument("Address", type=str, help="Address of user is required", required=True)

def handle_error(err):
    return f"{err.__class__.__name__}: {err}"

class User(Resource):
    user_db_method = UserDbMethodsNoSQL(db)

    def get(self):
        try:
            result = self.user_db_method.get_all_users()
            return result
        except Exception as e:
            print(e)
            return None
        
    def post(self):
        args = user_login_args.parse_args()
        try:
            user = self.user_db_method.login(username=args['Username'], password=args['Password'])
            if user is None:
                return abort(404, message='No password or username match found')
            return { "status": True, "message": "Login successfully!", "user": user}, 200
        except Exception as e:
            return handle_error(e)
            # return abort(400, message="Login failed")

    def put(self):
        args = user_put_args.parse_args()
        try:
            userExist = self.user_db_method.get_user_by_name(name=args['Name'])
            if userExist is not None:
                return { "status": False, "message": "User already exists"}, 400

            userObj = UserModel(name=args['Name'], email=args['Email'], username=args['Username'], password=args['Password'], phoneNumber=args['PhoneNumber'], address=args['Address'])
            user = self.user_db_method.regist_user(userObj)

            if user is None:
                return { "status": False, "message": "Couldn't create user"}, 409
            return { "status": True, "message": "Regist new user successfully!", "user": user}, 200
        except Exception as e:
            return handle_error(e)

todo_post_args = reqparse.RequestParser()
todo_post_args.add_argument("title", type=str, help="Title of task is required", required=True)
todo_post_args.add_argument("description", type=str, help="Description of task is required", required=True)

class ToDo(Resource):
    todo_db_methods = ToDoDbMethodsNoSQL(db)
    
    def get (self, user_id):
        try:
            results = self.todo_db_methods.get_task_by_user(user_id)
            return results
        except Exception as e:
            handle_error(e)

    def post(self, user_id):
        try:
            args = todo_post_args.parse_args()
            date_created = datetime.datetime.now()
            todo = ToDoModel(title = args["title"], description = args["description"], is_completed = False, creator = user_id, date_created = str(date_created))
            results = self.todo_db_methods.create_task(todo)
            if results is None:
                return {"status": False, "message": "Create task failed!"}, 409
            
            return {"status": True, "message": "Task created successfully"}, 200
        except Exception as e:
            print(e)
            handle_error(e)

api.add_resource(User, "/users")
api.add_resource(ToDo, "/todo/<user_id>")

if __name__ == '__main__':
    app.run(debug=True)