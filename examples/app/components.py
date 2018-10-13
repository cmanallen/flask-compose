from flask_router import Component
from models import UserModel, UserEmailModel, UserPhoneModel
from schemas import UserSchema, UserEmailSchema, UserPhoneSchema


class ActiveUserComponent(Component):
    """Generic component."""

    def make_query(self, model, **uri_args):
        """Return a query which fetches only active users."""
        query = self.parent.make_query(model, **uri_args)
        return query.filter(UserModel.is_active.is_(True))


class TypeComponent(Component):
    model = None
    schema = None

    @property
    def query(self):
        return self.model.query

    def make_query(self, query, **uri_args):
        """Return a query scoped by the uri args."""
        query = self.parent.make_query(query, **uri_args)
        for column, value in uri_args.items():
            query = query.filter(getattr(self.model, column) == value)
        return query


class UserComponent(TypeComponent):
    model = UserModel
    schema = UserSchema

    def schema_dump_options(self, **schema_options):
        schema_options['only'] = ('id',)
        return self.parent.schema_dump_options(**schema_options)


class UserUpdateComponent(Component):

    def schema_dump_options(self, **schema_options):
        schema_options['only'] = ('id', 'is_active')
        return self.parent.schema_dump_options(**schema_options)

    def schema_load_options(self, **schema_options):
        schema_options['only'] = ('id', 'is_active')
        return self.parent.schema_load_options(**schema_options)


class UserChildMixin:

    @property
    def query(self):
        return self.model.query.join(UserModel)


class UserEmailComponent(UserChildMixin, TypeComponent):
    model = UserEmailModel
    schema = UserEmailSchema


class UserPhoneComponent(UserChildMixin, TypeComponent):
    model = UserPhoneModel
    schema = UserPhoneSchema
