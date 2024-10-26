from . import main
from  flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Todo


@main.route('/')
@main.route('/index')
@login_required
def index():
    return render_template('index.html', title='Todo App' , todos=Todo.query.filter_by(user_id=current_user.id).all())

