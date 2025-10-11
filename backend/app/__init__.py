from flask import Flask
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    CORS(app, 
         origins=["http://localhost:5173", "http://127.0.0.1:5173"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"])
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    
    from app import routes
    app.register_blueprint(routes.bp)
    
    if not os.path.exists('data'):
        os.makedirs('data')
    
    return app