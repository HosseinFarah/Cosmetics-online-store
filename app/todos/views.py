from . import todos
from flask import render_template, request, redirect, url_for, flash
from app import db
from app.models import Todo
from flask_login import login_required, current_user
from datetime import datetime
from ..forms import NewTodoForm, UpdateTodoForm

@todos.route('new_todo', methods=['GET', 'POST'])
@login_required
def new_todo():
    form = NewTodoForm()
    if form.validate_on_submit():
        todo = Todo(
            title=form.title.data,
            description=form.description.data,
            user_id=current_user.id,
            status= form.status.data,
            due_date=form.due_date.data,
        )
        db.session.add(todo)
        db.session.commit()
        flash('Todo added successfully', 'success')
        return redirect(url_for('main.index'))
    return render_template('todos/new_todo.html', form=form)
        
@todos.route('update_todo/<int:id>', methods=['GET', 'POST'])
@login_required
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    form = UpdateTodoForm()
    if form.validate_on_submit():
        todo.title = form.title.data
        todo.description = form.description.data
        todo.status = form.status.data
        todo.due_date = form.due_date.data
        db.session.commit()
        flash('Todo updated successfully', 'success')
        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        form.title.data = todo.title
        form.description.data = todo.description
        form.status.data = todo.status
        form.due_date.data = todo.due_date
    return render_template('todos/update_todo.html', form=form) 

@todos.route('delete_todo/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted successfully', 'success')
    return redirect(url_for('main.index'))
