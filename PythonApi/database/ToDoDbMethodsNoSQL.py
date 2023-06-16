from bson.json_util import dumps, loads
from models.ToDo import ToDoModel
from database.UserDbMethodsNoSQL import UserDbMethodsNoSQL

class ToDoDbMethodsNoSQL():
    def __init__(self, db):
        self.db = db

    def get_task_by_user(self, userId):
        todos = self.db.todos.find({"creator": userId}).limit(10)
        result = dumps(todos)
        return result
    
    def create_task(self, todo: ToDoModel):
        print(todo)
        creator = UserDbMethodsNoSQL.get_user_by_id(userID = todo['creator'])
        # self.db.todos.insert_one({
        #     "title": todo.title,
        #     "description": todo.description,
        #     "is_completed": todo.is_completed,
        #     "creator": todo.creator,
        #     "date_created": todo.date_created,
        # })
        # todoDetail = self.db.todo.find_one({"title": todo.title})
        # if todoDetail is None:
        #     return None
        return creator
    