from . import main
from  flask import render_template, redirect, url_for, request, flash, current_app, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Todo
from app import db
from app.models import Product, Category

# @main.route('/')
# @main.route('/index')
# @login_required
# def index():
#     return render_template('index.html', title='Todo App' , todos=Todo.query.filter_by(user_id=current_user.id).all())


@main.route("/")
@main.route("/index")
def index():
    products = db.session.query(Product).all()
    categories = db.session.query(Category).all()
    sliders = ['(1).webp', '(2).webp', '(3).webp', '(4).webp']
    return render_template("index.html", products=products, categories=categories, sliders=sliders)
