from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from datetime import date

from applications.database import db

class User(db.Model):
    __tablename__="user"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String, nullable=False, unique=True) #This name is username
    password=db.Column(db.String, nullable=False)
    role=db.Column(db.String)

class Category(db.Model):
    __tablename__="category"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String, nullable=False, unique=True)
    products=db.relationship('Product', backref='category')

class Product(db.Model):
    __tablename__="product"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String, nullable=False, unique=True)
    exp_date=db.Column(db.Date, nullable=False)
    rate_per_unit=db.Column(db.Integer, nullable=False)
    qnt_avl=db.Column(db.Integer)
    cat_id=db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
class Order(db.Model):
    __tablename__="order"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id=db.Column(db.Integer, nullable=False)
    product_name=db.Column(db.String, nullable=False)
    user_id=db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.Date, nullable=False, default=date.today)