#import flask dependancy 
from flask import Flask

#create new flask app instance
app = Flask(__name__)

#create route
@app.route('/')
def hello_world():
    return 'Hello world'