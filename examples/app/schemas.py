import marshmallow as ma


class UserSchema(ma.Schema):
    id = ma.fields.Integer()
    username = ma.fields.String()
    is_active = ma.fields.Boolean()


class UserEmailSchema(ma.Schema):
    id = ma.fields.Integer()
    email_address = ma.fields.String()
    is_confirmed = ma.fields.Boolean()
    user_id = ma.fields.Integer()


class UserPhoneSchema(ma.Schema):
    id = ma.fields.Integer()
    phone_number = ma.fields.String()
    user_id = ma.fields.Integer()
