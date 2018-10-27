from app.common import db


class UserModel(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=True, nullable=False)


class UserEmailModel(db.Model):
    __tablename__ = 'user_email'

    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(128))
    is_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('UserModel')


class UserPhoneModel(db.Model):
    __tablename__ = 'user_phone'

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(128))
    is_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('UserModel')
