from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    steam_id = db.Column(db.String(64), unique=True,  nullable=False)
    steam_username = db.Column(db.String(128), nullable=False)
    steam_avatar_url = db.Column(db.String(256))
    credit_balance = db.Column(db.Numeric(10, 2), default=0.00)
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'<User {self.steam_username}>'
    
    class SkinDeposit(db.Model):
        __tablename__ = 'skin_deposits'
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        skin_name = db.Column(db.String(256), nullable=False)
        skin_exterior = db.Column(db.String(64))
        appraised_value = db.Column(db.Numeric(10, 2), nullable=False)
        credits_issued = db.Column(db.Numeric(10, 2), nullable=False)
        status = db.Column(db.String(32), default='pending')
        deposited_at = db.Column(db.DateTime, default=datetime.now)

        user = db.relationship('User', backref='deposits')

        def __repr__(self):
            return f'<SkinDeposit {self.skin.name} - {self.status}>'