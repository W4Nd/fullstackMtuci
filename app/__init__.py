from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()
secret_key = os.environ.get('SECRET_KEY')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    
    from app import routes
    app.register_blueprint(routes.bp)
    
    if not os.path.exists('data'):
        os.makedirs('data')
    
    return app