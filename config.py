import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI ='postgresql://u5uqur5natjbdu:p421e5dfb4ca13eef225f8c015da4ceb9682fae8be251ccddc64a5ea3732b7278@c97r84s7psuajm.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d3b4f47b5ibc0p'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
