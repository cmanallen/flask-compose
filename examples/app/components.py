from flask_router import Component
from models import UserModel, UserEmailModel
from schemas import UserSchema, UserEmailSchema


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

    @property
    def schema_dump_options(self):
        options = self.parent.schema_dump_options
        options['only'] = ('id',)
        return options


class UserEmailComponent(TypeComponent):
    model = UserEmailModel
    schema = UserEmailSchema

    @property
    def query(self):
        return self.model.query.join(UserModel)
