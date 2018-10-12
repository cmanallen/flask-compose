from common import db


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=False, nullable=False)


class UserEmailModel(db.Model):
    __tablename__ = 'user_email'

    id = db.Column(db.Integer, primary_key=True)
    is_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('UserModel')
