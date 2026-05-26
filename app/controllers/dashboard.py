from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..extensions import db
from ..models.quote import Quote, QuoteStatus

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@bp.route('/')
@login_required
def index():
    quotes = Quote.query.filter_by(user_id=current_user.id).all()
    total_quotes = len(quotes)
    accepted = [q for q in quotes if q.status == QuoteStatus.ACCEPTED]
    pending = [q for q in quotes if q.status in (QuoteStatus.DRAFT, QuoteStatus.SENT)]
    total_value = sum(q.total for q in accepted)
    recent = sorted(quotes, key=lambda q: q.created_at, reverse=True)[:5]
    return render_template('dashboard/index.html',
        total_quotes=total_quotes,
        accepted=len(accepted),
        pending=len(pending),
        total_value=total_value,
        recent_quotes=recent
    )
