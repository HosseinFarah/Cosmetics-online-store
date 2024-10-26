from flask import Blueprint

todos = Blueprint('todos', __name__)

from . import views