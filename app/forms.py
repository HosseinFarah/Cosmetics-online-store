from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, IntegerField, DateField, FileField, HiddenField,RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from app.models import User, Todo
from flask_login import current_user
from flask_wtf.file import FileAllowed, FileRequired
import re

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
    
# Custom validator for image size
def img_size(max_size, message=None):
    def _img_size(form, field):
        if field.data:
            field.data.seek(0, 2)  # Seek to end of file
            size = field.data.tell()
            if size > max_size:
                raise ValidationError(message or 'File size must be less than %d bytes' % max_size)
    return _img_size

class RegistrationForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=100), Regexp("^[a-zåäöA-ZÅÄÖ'\\-]+$", message='Only letters, hyphens and apostrophes allowed')])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=100), Regexp("^[a-zåäöA-ZÅÄÖ'\\-]+$", message='Only letters, hyphens and apostrophes allowed')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password',validators=[DataRequired(),Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;:'\",.<>?/])[A-Za-z\d!@#$%^&*()_+\-=\[\]{}|;:'\",.<>?/]{8,}$",message='Password must contain at least one uppercase letter, one lowercase letter, one number, one special character, and be at least 8 characters long')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    address = StringField('Address', validators=[DataRequired(),Regexp("^[a-zåäöA-ZÅÄÖ0-9'\\- ]+$", message='Only letters, numbers, hyphens and apostrophes allowed')])
    zipcode = StringField('Zip Code', validators=[DataRequired(),Regexp("^[0-9]{5}$", message='Zip code must be 5 digits long')])
    # define phone number Regex pattern accepted numbers and - or space and + and () max 15 digits
    phone = StringField('Phone Number', validators=[DataRequired(),Regexp("^[\d\s\-\+\(\)]{1,15}$", message='Phone number must have at most 15 digits and can contain numbers, spaces, hyphens, plus signs and parentheses')])
    image = FileField('Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Only jpg, png, jpeg and gif files allowed'), FileRequired(),img_size(1*1024*1024, message='Image size must be less than 1MB')])
    submit = SubmitField('Sign Up')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use. Please choose a different one.')
        
    def validate_phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('Phone number already in use. Please choose a different one.')
   
class UpdateAccountForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=100), Regexp("^[a-zåäöA-ZÅÄÖ'\\-]+$", message='Only letters, hyphens and apostrophes allowed')])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=100), Regexp("^[a-zåäöA-ZÅÄÖ'\\-]+$", message='Only letters, hyphens and apostrophes allowed')])
    address = StringField('Address', validators=[DataRequired(),Regexp("^[a-zåäöA-ZÅÄÖ0-9'\\- ]+$", message='Only letters, numbers, hyphens and apostrophes allowed')])
    zipcode = StringField('Zip Code', validators=[DataRequired(),Regexp("^[0-9]{5}$", message='Zip code must be 5 digits long')])
    phone = StringField('Phone Number', validators=[DataRequired(),Regexp("^[\d\s\-\+\(\)]{1,15}$", message='Phone number must have at most 15 digits and can contain numbers, spaces, hyphens, plus signs and parentheses')])
    image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'gif'], 'Only jpg, png, jpeg and gif files allowed')])
    submit = SubmitField('Update')
    
        
    def validate_phone(self, phone):
        if phone.data != current_user.phone:
            user = User.query.filter_by(phone=phone.data).first()
            if user:
                raise ValidationError('Phone number already in use. Please choose a different one.')
            
            
class NewTodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=100), Regexp("^[a-zåäöA-ZÅÄÖ0-9'\\- ]+$", message='Only letters, numbers, hyphens and apostrophes allowed')])
    description = TextAreaField('Description', validators=[DataRequired(), Regexp("^[a-zåäöA-ZÅÄÖ0-9'\\- ]+$", message='Only letters, numbers, hyphens and apostrophes allowed')])
    status = SelectField('Status', choices=[('pending', 'Pending'), ('inprogress', 'In Progress'), ('completed', 'Completed')], validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Create')

class UpdateTodoForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=100), Regexp("^[a-zåäöA-ZÅÄÖ0-9'\\- ]+$", message='Only letters, numbers, hyphens and apostrophes allowed')])
    description = TextAreaField('Description', validators=[DataRequired(), Regexp("^[a-zåäöA-ZÅÄÖ0-9'\\- ]+$", message='Only letters, numbers, hyphens and apostrophes allowed')])
    status = SelectField('Status', choices=[('pending', 'Pending'), ('inprogress', 'In Progress'), ('completed', 'Completed')], validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Update')
    
class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
        
class ChangePasswordForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired(),Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;:'\",.<>?/])[A-Za-z\d!@#$%^&*()_+\-=\[\]{}|;:'\",.<>?/]{8,}$",message='Password must contain at least one uppercase letter, one lowercase letter, one number, one special character, and be at least 8 characters long')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
    
class ResetEmailRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Email Reset')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None and user.email != current_user.email:
            raise ValidationError('This email is already in use. Please choose a different one.')


        
        
class ResetEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Email')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use. Please choose a different one.')
        

    
class UpdateUserByAdmin(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=100), Regexp("^[a-zåäöA-ZÅÄÖ'\\-]+$", message='Only letters, hyphens and apostrophes allowed')])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=100), Regexp("^[a-zåäöA-ZÅÄÖ'\\-]+$", message='Only letters, hyphens and apostrophes allowed')])
    address = StringField('Address', validators=[DataRequired(),Regexp("^[a-zåäöA-ZÅÄÖ0-9'\\- ]+$", message='Only letters, numbers, hyphens and apostrophes allowed')])
    zipcode = StringField('Zip Code', validators=[DataRequired(),Regexp("^[0-9]{5}$", message='Zip code must be 5 digits long')])
    role = SelectField('Role', choices=[('User', 'User'), ('Moderator', 'Moderator'), ('Administrator', 'Administrator')], validators=[DataRequired()])
    is_active = BooleanField('is_active')
    submit = SubmitField('Update')
    
    
    

     
        
class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')
    
    def validate_search(self, search):
        if search.data == '':
            raise ValidationError('You must enter a search term.')


class UpdatePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password',validators=[DataRequired(),Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+\-=\[\]{}|;:'\",.<>?/])[A-Za-z\d!@#$%^&*()_+\-=\[\]{}|;:'\",.<>?/]{8,}$",message='Password must contain at least one uppercase letter, one lowercase letter, one number, one special character, and be at least 8 characters long')])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')
        
