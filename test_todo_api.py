import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from create_app import create_app
from models.todo_model import TodoModel

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def todo_model():
    return TodoModel()

def test_create_todo(client, todo_model):
    response = client.post('/todos', json={'task': 'Test Todo'})
    assert response.status_code == 201
    assert 'task' in response.json
    assert response.json['task'] == 'Test Todo'

def test_get_all_todos(client, todo_model):
    client.post('/todos', json={'task': 'Test Todo'})
    response = client.get('/todos')
    assert response.status_code == 200
    assert len(response.json) > 0

def test_get_todo_by_id(client, todo_model):
    todo = client.post('/todos', json={'task': 'Test Todo'})
    todo_id = todo.json['_id']
    response = client.get(f'/todos/{todo_id}')
    assert response.status_code == 200
    assert response.json['_id'] == todo_id

def test_update_todo(client, todo_model):
    todo = client.post('/todos', json={'task': 'Test Todo'})
    todo_id = todo.json['_id']
    response = client.put(f'/todos/{todo_id}', json={'task': 'Updated Todo', 'done': True})
    assert response.status_code == 200
    assert response.json['task'] == 'Updated Todo'
    assert response.json['done'] is True

def test_delete_todo(client, todo_model):
    todo = client.post('/todos', json={'task': 'Test Todo'})
    todo_id = todo.json['_id']
    response = client.delete(f'/todos/{todo_id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Todo deleted successfully'
