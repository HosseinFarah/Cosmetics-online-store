from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import login, db
from ..forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, UpdateAccountForm, ResetEmailRequestForm, ResetEmailForm,UpdateUserByAdmin,SearchForm,UpdatePasswordForm
from app.auth import auth
from werkzeug.utils import secure_filename
import os
from app.email import send_email
from pytz import timezone
from datetime import datetime
from ..decorators import permission_required, admin_required
from app.models import Role


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        if not current_user.is_confirmed and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
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
            #last_login 
            current_user.ping()
            next_page = request.args.get('next')
            if next_page and not next_page.startswith('/'):
                next_page = None
            return redirect(next_page or url_for('main.index'))
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
        db.session.commit()
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
    else:
        flash('Something went wrong. Please try again.', 'danger')
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


@auth.route('/all_users', methods=['GET', 'POST'])
@login_required
@admin_required
def all_users():
    search = request.args.get('search', '')
    page=request.args.get('page', 1, type=int)
    per_page = 15
    all_users_count = User.query.count()
    if search:
        query = User.query.filter(User.firstname.like(f'%{search}%') | User.lastname.like(f'%{search}%') | User.email.like(f'%{search}%')| User.phone.like(f'%{search}%'))
    else:
        query = User.query

    sort_by = request.args.get('sort_by', 'firstname')
    order = request.args.get('order', 'asc')

    if order == 'asc':
        query = query.order_by(getattr(User, sort_by).asc())
    else:
        query = query.order_by(getattr(User, sort_by).desc())
    
    users = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('auth/all_users.html', users=users, search=search, page=page, pages=users.pages, all_users=all_users_count,order=order, sort_by=sort_by)

@auth.route('/edit_user_admin/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user_admin(id):
    user = User.query.get(id)
    form = UpdateUserByAdmin()
    if form.validate_on_submit():
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.address = form.address.data
        user.zipcode = form.zipcode.data
        role = Role.query.filter_by(name=form.role.data).first()
        user.is_active = form.is_active.data
        user.role = role
        
        try:
            db.session.commit()
            flash('User has been updated.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating user.', 'danger')
        return redirect(url_for('auth.all_users'))
    
    elif request.method == 'GET':
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.address.data = user.address
        form.zipcode.data = user.zipcode
        form.role.data = user.role.name if user.role else 'User'
        form.is_active.data = user.is_active
    return render_template('auth/edit_user_admin.html', form=form, user=user)


@auth.route('/delete_user_admin/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_user_admin(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    flash('User has been deleted.', 'success')
    return redirect(url_for('auth.all_users'))

@auth.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.password = form.new_password.data
            try:
                db.session.commit()
                flash('Your password has been updated.', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while updating your password.', 'danger')
        else:
            flash('Invalid old password.', 'danger')
    return render_template('auth/update_password.html', form=form)

@auth.route('/reset_email_request', methods=['GET', 'POST'])
@login_required
def reset_email_request():
    form = ResetEmailRequestForm()
    if form.validate_on_submit():
        token = current_user.generate_email_change_token(form.email.data)
        send_email(form.email.data, 'Confirm Your Email Address', 'auth/email/change_email', user=current_user, token=token)
        flash('An email with instructions to confirm your new email address has been sent to you.', 'info')
        return redirect(url_for('auth.profile'))
    return render_template('auth/reset_email_request.html', form=form)

@auth.route('/change_email/<token>', methods=['GET', 'POST'])
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.', 'success')
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
    return redirect(url_for('auth.profile'))


        
