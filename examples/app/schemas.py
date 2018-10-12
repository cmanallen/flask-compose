import marshmallow as ma


class UserSchema(ma.Schema):
    id = ma.fields.Integer(dump_only=True)
    is_active = ma.fields.Boolean()


class UserEmailSchema(ma.Schema):
    id = ma.fields.Integer(dump_only=True)
    user_id = ma.fields.Integer()

