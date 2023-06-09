from flask import jsonify
from database.IUserDbMethods import IUserDbMethods
from bson.json_util import dumps
import bcrypt

class UserDbMethodsNoSQL (IUserDbMethods):
    def __init__(self, db):
        super().__init__(db)
        self.db = db

    def get(self):
        users = self.db.users.find({}, {'username': 1, 'email': 1, 'phoneNumber': 1, 'address': 1})
        result = dumps(users)
        return result
    
    def login(self, username, password):
        user = self.db.users.find_one({'username': username}, {'username': 1, 'password': 1})
        if user is not None:
            print('come here')
            user = jsonify(user)
            if bcrypt.checkpw(password, user.password):
                return user
            else:
                return None
        return None
