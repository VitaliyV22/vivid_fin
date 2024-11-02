from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

print("SECRET_KEY:", os.environ.get('SECRET_KEY'))  # Debug print
print("SQLALCHEMY_DATABASE_URI:", os.environ.get('SQLALCHEMY_DATABASE_URI'))  # Debug print

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
