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
        

    class Trade(db.Model):
        __tablename__ = 'trades'
        id = db.Column(db.Integer, primary_key=True)
        skin_name = db.Column(db.String(256), nullable=False)
        buy_price = db.Column(db.Numeric(10, 2), nullable=False)
        sell_price = db.Column(db.Numeric(10, 2))
        profit = db.Column(db.Numeric(10, 2))
        status = db.Column(db.String(32), default='open')
        opened_at = db.Column(db.DateTime, default=datetime.now)
        closed_at = db.Column(db.DateTime)

        allocations = db.relationship('TradeAllocation', backref='trade')

        def __repr__(self):
            return f'<Trade {self.skin_name} - {self.status}>'
        

    class TradeAllocation(db.Model):
        __tablename__ = 'trade_allocations'

        id = db.Column(db.Integer, primary_key=True)
        trade_id = db.Column(db.Integer, db.ForeignKey('trades.id'), nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        credits_allocated = db.Column(db.Numeric(10, 2), nullable=False)
        profit_share = db.Column(db.Numeric(10, 2))
        platform_fee = db.Column(db.Numeric(10, 2))

        user = db.relationship('User', backref='allocations')

        def __repr__(self):
            return f'<TradeAllocation user={self.user_id} trade={self.trade_id}>'
    

    class WithdrawalRequest(db.Model):
        __tablename__ = 'withdrawal_requests'

        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        credits_spent = db.Column(db.Numeric(10, 2), nullable=False)
        skin_name = db.Column(db.String(256), nullable=False)
        status = db.Column(db.String(32), default='pending')
        requested_at = db.Column(db.DateTime, default=datetime.now)
        fulfilled_at = db.Column(db.DateTime)

        # TODO: Bot will automatically find skin(s) within 1% of credits_spent
        # If none available in inventory, bot will purchase from Skinport
        # May need withdrawal_items table to track multiple skins per withdrawa

        user = db.relationship('User', backref='withdrawals')

        def __repr__(self):
            return f'<WithdrawalRequest {self.skin_name} - {self.status}>'