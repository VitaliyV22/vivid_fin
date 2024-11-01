import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI ='postgresql://postgres:3znwxX6pV9OsQK9l5v1qvividfin.cdqg4cemyblo.us-east-1.rds.amazonaws.com:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


