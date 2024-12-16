from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# Configuration for MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/todo_db"
mongo = PyMongo(app)

todo_collection = mongo.db.todos

# Serve the frontend
@app.route('/')
def index():
    return render_template('index.html')

# 1. Add a new To-Do Task
@app.route('/todo', methods=['POST'])
def add_todo():
    data = request.json
    if not data or 'task' not in data:
        return jsonify({"error": "Task content is required"}), 400

    task = {
        "task": data['task'],
        "completed": data.get('completed', False)
    }
    result = todo_collection.insert_one(task)
    return jsonify({"message": "Task added", "id": str(result.inserted_id)}), 201

# 2. Display list of To-Do Tasks
@app.route('/todos', methods=['GET'])
def get_todos():
    tasks = []
    for task in todo_collection.find():
        tasks.append({
            "id": str(task["_id"]),
            "task": task["task"],
            "completed": task["completed"]
        })
    return jsonify(tasks), 200

# 3. Edit a particular To-Do Task
@app.route('/todo/<id>', methods=['PUT'])
def edit_todo(id):
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    update_data = {}
    if 'task' in data:
        update_data['task'] = data['task']
    if 'completed' in data:
        update_data['completed'] = data['completed']

    if not update_data:
        return jsonify({"error": "No valid fields to update"}), 400

    result = todo_collection.update_one({"_id": ObjectId(id)}, {"$set": update_data})

    if result.matched_count == 0:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task updated"}), 200

# 4. Delete a particular To-Do Task
@app.route('/todo/<id>', methods=['DELETE'])
def delete_todo(id):
    result = todo_collection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        return jsonify({"error": "Task not found"}), 404

    return jsonify({"message": "Task deleted"}), 200

# 5. Delete all To-Do Tasks
@app.route('/todos', methods=['DELETE'])
def delete_all_todos():
    todo_collection.delete_many({})
    return jsonify({"message": "All tasks deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
