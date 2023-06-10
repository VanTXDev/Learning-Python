from flask import jsonify
from database.IUserDbMethods import IUserDbMethods
from bson.json_util import dumps, loads
import bcrypt
from models.User import UserModel

class UserDbMethodsNoSQL (IUserDbMethods):
    def __init__(self, db):
        super().__init__(db)
        self.db = db

    def get(self):
        users = self.db.users.find({}, {'username': 1, 'email': 1, 'phoneNumber': 1, 'address': 1})
        result = dumps(users)
        return result
    
    def login(self, username, password):
        user = self.db.users.find_one({'username': username}, {'username': 1, 'password': 1, 'email': 1, '_id': 0})
        if user is not None:
            user = dumps(user)
            userCheck = loads(user)
            passEncode = str(password).encode()
            if bcrypt.checkpw(passEncode, userCheck['password']):
                return user
        return None
    
    def put(self, user: UserModel):
        saltp = bcrypt.gensalt(14)
        passwordHashed = bcrypt.hashpw(user.password.encode(), saltp)
        self.db.users.insert_one({
            "name": user.name,
            "email": user.email,
            "username": user.username,
            "password": passwordHashed,
            "phoneNumber": user.phoneNumber,
            "address": user.address
        })
        userDetail = self.get_user_by_name(name=user.name)
        if userDetail is None:
            return None
        return userDetail

    def get_user_by_name(self, name):
        user = self.db.users.find_one_or_404({'name': name}, {'username': 1, 'email': 1, 'phoneNumber': 1, 'address': 1})
        if user is not None:
            result = dumps(user)
            return result
        return None