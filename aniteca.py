
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_pyfile('config.py')
db = SQLAlchemy(app)


from routes import *



if __name__ == "__main__":
    db.create_all()
    app.run(host="0.0.0.0",port=8080, debug=True)