import csv
from flask import Blueprint, render_template, redirect, url_for, flash, request,session,Response
from app import db, bcrypt
from flask_login import login_user, logout_user, login_required,current_user
from app.models.user import User
from app.models.user import Prediction
from .forms import RegisterForm, LoginForm



admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'admin' and password == 'admin':
            session['admin_logged_in'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('admin/login.html')

@admin_bp.route('/dashboard')
def dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    return render_template('admin/dashboard.html')

@admin_bp.route('/users')
def view_users():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    users = User.query.all()
    return render_template('admin/view_users.html', users=users)

@admin_bp.route('/predictions')
def prediction_logs():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    predictions = Prediction.query.order_by(Prediction.timestamp.desc()).all()
    return render_template('admin/prediction_logs.html', predictions=predictions)

@admin_bp.route('/export')
def export_csv():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    predictions = Prediction.query.all()
    def generate():
        data = [['User ID', 'Filename', 'Accuracy', 'FPS', 'Confidence', 'Timestamp']]
        for p in predictions:
            data.append([
                p.user_id,
                p.filename,
                f"{p.accuracy:.2f}",
                f"{p.fps:.2f}",
                f"{p.confidence:.2f}",
                p.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            ])
        for row in data:
            yield ','.join(row) + '\n'
    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=predictions.csv"})

@admin_bp.route('/accuracy-graph')
def accuracy_graph():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin.login'))
    predictions = Prediction.query.order_by(Prediction.timestamp).all()
    timestamps = [p.timestamp.strftime("%Y-%m-%d %H:%M:%S") for p in predictions]
    accuracies = [p.accuracy for p in predictions]
    return render_template('admin/accuracy_graph.html', labels=timestamps, data=accuracies)