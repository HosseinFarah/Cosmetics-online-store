from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import login, db
from ..forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, UpdateAccountForm, ResetEmailRequestForm, ResetEmailForm
from app.auth import auth
from werkzeug.utils import secure_filename
import os
from app.email import send_email
from pytz import timezone
from datetime import datetime

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_login = datetime.now(timezone('Europe/Helsinki'))
        db.session.commit()
        
@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.is_confirmed and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))
    

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.is_confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.index'))
        flash('Invalid email or password.', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@auth.route('auth/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, password=form.password.data, address=form.address.data, zipcode=form.zipcode.data, phone=form.phone.data, image=filename)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent via email.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.is_confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent via email.', 'info')
    return redirect(url_for('main.index'))

@auth.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password', 'auth/email/reset_password', user=user, token=token)
        flash('An email with instructions to reset your password has been sent to you.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', title='Reset Password', form=form)
    
@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            flash('Your password has been updated.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('The reset password link is invalid or has expired.', 'danger')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)    
          
@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user=current_user
    return render_template('auth/profile.html', title='Profile', user=user)

@auth.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    image=None
    form = UpdateAccountForm()
    if form.validate_on_submit():
        print("Form validated successfully")
        if request.files['image']:
            image = request.files['image']
            if image:
                filename = secure_filename(image.filename)
                image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                current_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.image)
                if current_user.image != 'default.jpg' and current_user.image != filename:
                    if os.path.exists(current_image_path):
                        os.remove(current_image_path)
                current_user.image = filename
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.address = form.address.data
        current_user.zipcode = form.zipcode.data
        current_user.phone = form.phone.data
        try:
            db.session.commit()
            print("Database commit successful")
            flash('Your profile has been updated.', 'success')
        except Exception as e:
            db.session.rollback()
            print(f"Database commit failed: {e}")
            flash('An error occurred while updating your profile.', 'danger')
        return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.address.data = current_user.address
        form.zipcode.data = current_user.zipcode
        form.phone.data = current_user.phone
    else:
        print("Form validation failed")
        print(form.errors)
    return render_template('auth/update_profile.html', form=form)