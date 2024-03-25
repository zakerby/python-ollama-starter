from flask import Flask

app = Flask(__name__)

def run():
    """
        Initialize the flask app and run it
    """
    app.config['ENV'] = 'development'
    
    return app