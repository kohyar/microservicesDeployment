import os

class Config(object):
    basedir = os.path.abspath(os.path.dirname(__file__))
    movies_url = "http://127.0.0.1:5000"




    # Uncomment the desired option
    deploy = 'docker'   # deploying on docker using mysql
    # deploy = 'mysql_local' # deploying locally using mysql
    # deploy = 'sqlite_local' # deploying locally using sqlite

    SQLALCHEMY_DATABASE_URI = ''

    if deploy == 'docker':
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://evaluations:evaluations@db_evaluations/evaluations'
        movies_url = "http://movies:5000"
    elif deploy == 'mysql_local':
        SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://evaluations:evaluations@localhost:3306/evaluations'
    elif deploy == 'sqlite_local':
        SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    else:
        print("Wrong deployment option.")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
