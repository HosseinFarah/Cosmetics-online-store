from . import db
import sqlalchemy as sa
import sqlalchemy.orm as so
from pytz import timezone
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False,index=True)
    lastname = db.Column(db.String(100), nullable=False,index=True)
    email = db.Column(db.String(100), unique=True, nullable=False,index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone=db.Column(db.String(20), nullable=False, unique=True,index=True)
    address=db.Column(db.String(255), nullable=False)
    zipcode=db.Column(db.String(15), nullable=False)
    image = db.Column(db.String(255), nullable=False, default='default.jpg')
    created_at = db.Column(db.DateTime, default=datetime.now(timezone('Europe/Helsinki')))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone('Europe/Helsinki')))
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    is_confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'),default=1)
    role = db.relationship('Role', backref=so.backref('users', lazy='dynamic'))
    user_todos = db.relationship('Todo', backref='user', lazy='dynamic')
    last_login = db.Column(db.DateTime, default=datetime.now(timezone('Europe/Helsinki')))
    
    def __repr__(self) -> str:
        return '<User %r>' % self.email
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def generate_confirmation_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm': self.id})
    

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token,max_age=3600)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.is_confirmed = True
        db.session.add(self)
        db.session.commit()
        return True
        
            
    
    def generate_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'reset': self.id})
    

    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token,max_age=3600)
        except:
            return False
        user = User.query.get(data.get('reset'))
        if user is None:
            return False
        user.password_hash = generate_password_hash(new_password)
        db.session.add(user)
        db.session.commit()
        return True
    
    def generate_email_change_token(self, new_email):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'change_email': self.id, 'new_email': new_email})
    
    @staticmethod
    def change_email(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token,max_age=3600)
        except:
            return False
        user = User.query.get(data.get('change_email'))
        new_email = data.get('new_email')
        if user is None or new_email is None:
            return False
        user.email = new_email
        db.session.add(user)
        db.session.commit()
        return True
    
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    def __repr__(self) -> str:
        return '<Role %r>' % self.name

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending', index=True)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone('Europe/Helsinki')))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone('Europe/Helsinki')))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone('Europe/Helsinki')))
    
    def __repr__(self) -> str:
        return '<Todo %r>' % self.title

