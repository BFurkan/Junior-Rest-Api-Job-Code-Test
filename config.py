import os

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'mysql://username:password@localhost/database_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
