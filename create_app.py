from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app():
    app = Flask(__name__)
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/myDatabase'
    mongo.init_app(app)

    # Import and register your blueprints/routes after initializing the app
    from routes.todo_routes import todo_routes
    app.register_blueprint(todo_routes)

    return app
