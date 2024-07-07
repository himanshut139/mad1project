from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from applications.database import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///groceasy_database.sqlite3"
app.config['SECRET_KEY'] = 'groceasysecretkey'
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = "./static/img/"


db.init_app(app)
app.app_context().push()  


from applications.controllers import *

if __name__ == "__main__":
    db.create_all()
    app.run()