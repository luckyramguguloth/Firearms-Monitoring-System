import csv
from flask import Blueprint, render_template, redirect, url_for, flash, request,session,Response
from app import db, bcrypt
from flask_login import login_user, logout_user, login_required,current_user
from app.models.user import User
from app.models.user import Prediction
from .forms import RegisterForm, LoginForm



auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Log!', 'success')
            return redirect(url_for('auth.dashboard'))  # placeholder for now
        else:
            flash('Login Failed. Check email and password.', 'danger')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)




@auth.route('/user_details')
@login_required
def user_details():
    return render_template('user_details.html', user=current_user)


@auth.route('/')
def index():
    return render_template('index.html') 