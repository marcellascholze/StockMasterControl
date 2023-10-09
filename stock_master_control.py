from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


from views import *
from auth import *

if(__name__ == '__main__'):
    app.run(host='localhost', port=8000, debug=True)