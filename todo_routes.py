from flask import Blueprint, jsonify, request
from models.todo_model import TodoModel

todo_routes = Blueprint('todo_routes', __name__)

# Create an instance of TodoModel
todo_model = TodoModel()

@todo_routes.route('/todos', methods=['GET'])
def get_all_todos():
    todos = todo_model.get_all_todos()
    return jsonify(todos)

@todo_routes.route('/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    todo = todo_model.create_todo(data['task'])
    return jsonify(todo), 201

@todo_routes.route('/todos/<string:id>', methods=['GET'])
def get_todo(id):
    todo = todo_model.get_todo_by_id(id)
    if todo:
        return jsonify(todo)
    return jsonify({'message': 'Todo not found'}), 404

@todo_routes.route('/todos/<string:id>', methods=['PUT'])
def update_todo(id):
    data = request.get_json()
    updated_todo = todo_model.update_todo(id, data)
    if updated_todo:
        return jsonify(updated_todo)
    return jsonify({'message': 'Todo not found'}), 404

@todo_routes.route('/todos/<string:id>', methods=['DELETE'])
def delete_todo(id):
    result = todo_model.delete_todo(id)
    if result:
        return jsonify({'message': 'Todo deleted successfully'})
    return jsonify({'message': 'Todo not found'}), 404
