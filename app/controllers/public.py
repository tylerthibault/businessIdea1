from flask import Blueprint, render_template, redirect, url_for, request, abort
from ..extensions import db
from ..models.quote import Quote, QuoteStatus

bp = Blueprint('public', __name__)

@bp.route('/q/<token>')
def view(token):
    quote = Quote.query.filter_by(public_token=token).first_or_404()
    return render_template('quotes/public.html', quote=quote, QuoteStatus=QuoteStatus)

@bp.route('/q/<token>/respond', methods=['POST'])
def respond(token):
    quote = Quote.query.filter_by(public_token=token).first_or_404()
    if quote.status != QuoteStatus.SENT:
        abort(400)
    action = request.form.get('action')
    if action == 'accept':
        quote.status = QuoteStatus.ACCEPTED
    elif action == 'decline':
        quote.status = QuoteStatus.DECLINED
    db.session.commit()
    return redirect(url_for('public.view', token=token))
