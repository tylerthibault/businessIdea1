from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db
from ..models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        name = request.form.get('name', '').strip()
        pw = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'danger')
            return render_template('auth/register.html')
        user = User(email=email, name=name)
        user.set_password(pw)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Welcome to QuoteKit!', 'success')
        return redirect(url_for('dashboard.index'))
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        pw = request.form['password']
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(pw):
            flash('Invalid email or password.', 'danger')
            return render_template('auth/login.html')
        login_user(user, remember=request.form.get('remember'))
        return redirect(request.args.get('next') or url_for('dashboard.index'))
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('landing.index'))
