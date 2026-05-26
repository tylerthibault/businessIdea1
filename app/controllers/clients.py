from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from ..extensions import db
from ..models.client import Client

bp = Blueprint('clients', __name__, url_prefix='/clients')

@bp.route('/')
@login_required
def index():
    clients = Client.query.filter_by(user_id=current_user.id).order_by(Client.name).all()
    return render_template('clients/index.html', clients=clients)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        c = Client(
            user_id=current_user.id,
            name=request.form['name'],
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            company=request.form.get('company'),
            notes=request.form.get('notes'),
        )
        db.session.add(c)
        db.session.commit()
        flash('Client added!', 'success')
        return redirect(url_for('clients.index'))
    return render_template('clients/form.html', client=None)

@bp.route('/<int:client_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(client_id):
    client = Client.query.get_or_404(client_id)
    if client.user_id != current_user.id:
        abort(403)
    if request.method == 'POST':
        client.name = request.form['name']
        client.email = request.form.get('email')
        client.phone = request.form.get('phone')
        client.company = request.form.get('company')
        client.notes = request.form.get('notes')
        db.session.commit()
        flash('Client updated.', 'success')
        return redirect(url_for('clients.index'))
    return render_template('clients/form.html', client=client)

@bp.route('/<int:client_id>/delete', methods=['POST'])
@login_required
def delete(client_id):
    client = Client.query.get_or_404(client_id)
    if client.user_id != current_user.id:
        abort(403)
    db.session.delete(client)
    db.session.commit()
    flash('Client deleted.', 'info')
    return redirect(url_for('clients.index'))
