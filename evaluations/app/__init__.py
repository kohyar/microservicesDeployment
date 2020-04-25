from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
import logging as lg 
# from app.models import Movie



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from app import routes, models



# flask initdb
@app.cli.command()
def initdb():
    models.init_db()

    

# uncomment to initialize database automatically for
# every run
# models.init_db()