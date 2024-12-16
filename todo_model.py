from bson.objectid import ObjectId
from create_app import mongo  # Importing mongo instance from create_app.py

class TodoModel:
    def __init__(self):
        self.todos_collection = mongo.db.todos  # Accessing 'todos' collection in MongoDB

    def get_all_todos(self):
        todos = list(self.todos_collection.find())
        for todo in todos:
            todo['_id'] = str(todo['_id'])  # Convert ObjectId to string
        return todos

    def create_todo(self, task):
        todo = {'task': task, 'done': False}
        result = self.todos_collection.insert_one(todo)
        todo['_id'] = str(result.inserted_id)  # Convert ObjectId to string
        return todo

    def get_todo_by_id(self, id):
        todo = self.todos_collection.find_one({'_id': ObjectId(id)})
        if todo:
            todo['_id'] = str(todo['_id'])  # Convert ObjectId to string
        return todo

    def update_todo(self, id, data):
        updated_todo = self.todos_collection.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set': data},
            return_document=True
        )
        if updated_todo:
            updated_todo['_id'] = str(updated_todo['_id'])  # Convert ObjectId to string
        return updated_todo

    def delete_todo(self, id):
        result = self.todos_collection.delete_one({'_id': ObjectId(id)})
        return result.deleted_count > 0
