from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from .models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm
from . import db
from werkzeug.urls import url_parse

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('user.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@user_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.homepage'))

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('user.login'))
    return render_template('register.html', title='Register', form=form)


@user_bp.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect', 'danger')
            return redirect(url_for('user.change_password'))
        
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('change_password.html', title='Change Password', form=form)

@user_bp.route('/settings', methods=['GET', 'POST'])
def settings():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Current password is incorrect', 'danger')
            return redirect(url_for('user.change_password'))
        
        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('settings.html', title='Settings', form=form)

