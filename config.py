import os

SECRET_KEY = 'UniduniS'
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1q2w3e4r@localhost/flask'
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '\\uploads'