import enum
import secrets
from datetime import datetime
from ..extensions import db

class QuoteStatus(enum.Enum):
    DRAFT = 'draft'
    SENT = 'sent'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'
    EXPIRED = 'expired'

class Quote(db.Model):
    __tablename__ = 'quotes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(QuoteStatus), nullable=False, default=QuoteStatus.DRAFT)
    public_token = db.Column(db.String(64), unique=True, nullable=False, default=lambda: secrets.token_urlsafe(32))
    notes = db.Column(db.Text)
    valid_until = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    line_items = db.relationship('QuoteLineItem', backref='quote', lazy='dynamic',
                                 cascade='all, delete-orphan', order_by='QuoteLineItem.order')

    @property
    def subtotal(self):
        return sum(item.total for item in self.line_items)

    @property
    def total(self):
        return self.subtotal

    @property
    def status_badge_class(self):
        return {
            QuoteStatus.DRAFT: 'secondary',
            QuoteStatus.SENT: 'primary',
            QuoteStatus.ACCEPTED: 'success',
            QuoteStatus.DECLINED: 'danger',
            QuoteStatus.EXPIRED: 'warning',
        }.get(self.status, 'secondary')

    def __repr__(self):
        return f'<Quote {self.title}>'

class QuoteLineItem(db.Model):
    __tablename__ = 'quote_line_items'
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey('quotes.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    quantity = db.Column(db.Numeric(10, 2), nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    order = db.Column(db.Integer, default=0)

    @property
    def total(self):
        return float(self.quantity) * float(self.unit_price)
