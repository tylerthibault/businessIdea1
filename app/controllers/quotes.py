from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, send_file
from flask_login import login_required, current_user
from ..extensions import db
from ..models.quote import Quote, QuoteLineItem, QuoteStatus
from ..models.client import Client
import io

bp = Blueprint('quotes', __name__, url_prefix='/quotes')

def _owned_quote(quote_id):
    q = Quote.query.get_or_404(quote_id)
    if q.user_id != current_user.id:
        abort(403)
    return q

@bp.route('/')
@login_required
def index():
    quotes = Quote.query.filter_by(user_id=current_user.id).order_by(Quote.created_at.desc()).all()
    return render_template('quotes/index.html', quotes=quotes)

@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    clients = Client.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        q = Quote(
            user_id=current_user.id,
            title=request.form['title'],
            client_id=request.form.get('client_id') or None,
            notes=request.form.get('notes'),
        )
        db.session.add(q)
        db.session.commit()
        flash('Quote created!', 'success')
        return redirect(url_for('quotes.edit', quote_id=q.id))
    return render_template('quotes/form.html', quote=None, clients=clients)

@bp.route('/<int:quote_id>', methods=['GET', 'POST'])
@login_required
def edit(quote_id):
    quote = _owned_quote(quote_id)
    clients = Client.query.filter_by(user_id=current_user.id).all()
    if request.method == 'POST':
        quote.title = request.form.get('title', quote.title)
        quote.client_id = request.form.get('client_id') or None
        quote.notes = request.form.get('notes')
        vd = request.form.get('valid_until')
        if vd:
            from datetime import date
            try:
                quote.valid_until = date.fromisoformat(vd)
            except ValueError:
                pass
        else:
            quote.valid_until = None
        db.session.commit()
        flash('Quote updated.', 'success')
        return redirect(url_for('quotes.edit', quote_id=quote.id))
    return render_template('quotes/edit.html', quote=quote, clients=clients)

@bp.route('/<int:quote_id>/delete', methods=['POST'])
@login_required
def delete(quote_id):
    quote = _owned_quote(quote_id)
    db.session.delete(quote)
    db.session.commit()
    flash('Quote deleted.', 'info')
    return redirect(url_for('quotes.index'))

@bp.route('/<int:quote_id>/send', methods=['POST'])
@login_required
def send(quote_id):
    quote = _owned_quote(quote_id)
    quote.status = QuoteStatus.SENT
    db.session.commit()
    flash('Quote marked as sent.', 'success')
    return redirect(url_for('quotes.edit', quote_id=quote.id))

@bp.route('/<int:quote_id>/items', methods=['POST'])
@login_required
def add_line_item(quote_id):
    quote = _owned_quote(quote_id)
    desc = request.form.get('description', '').strip()
    if not desc:
        flash('Description is required.', 'warning')
        return redirect(url_for('quotes.edit', quote_id=quote.id))
    try:
        qty = float(request.form.get('quantity', 1))
        price = float(request.form.get('unit_price', 0))
    except ValueError:
        qty, price = 1.0, 0.0
    item = QuoteLineItem(quote_id=quote.id, description=desc, quantity=qty, unit_price=price)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('quotes.edit', quote_id=quote.id))

@bp.route('/<int:quote_id>/items/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_line_item(quote_id, item_id):
    quote = _owned_quote(quote_id)
    item = QuoteLineItem.query.get_or_404(item_id)
    if item.quote_id != quote.id:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('quotes.edit', quote_id=quote.id))

@bp.route('/<int:quote_id>/pdf')
@login_required
def pdf(quote_id):
    quote = _owned_quote(quote_id)
    from datetime import datetime as dt
    try:
        from weasyprint import HTML
        html_str = render_template('quotes/pdf.html', quote=quote, now=dt.utcnow())
        pdf_bytes = HTML(string=html_str).write_pdf()
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'quote-{quote.id}.pdf'
        )
    except Exception as e:
        flash(f'PDF generation failed: {e}', 'danger')
        return redirect(url_for('quotes.edit', quote_id=quote.id))
