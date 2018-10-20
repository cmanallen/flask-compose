from flask import request
from flask_router import Component

from models import UserModel, UserEmailModel, UserPhoneModel
from schemas import UserSchema, UserEmailSchema, UserPhoneSchema

import collections


class ActiveUserComponent(Component):
    """Generic component."""

    def make_query(self, model, **uri_args):
        """Return a query which fetches only active users."""
        query = self.parent.make_query(model, **uri_args)
        return query.filter(UserModel.is_active.is_(True))


class TypeComponent(Component):
    model = None
    schema = None
    jsonapi_type = None

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
    jsonapi_type = 'users'

    def schema_dump_options(self, **schema_options):
        schema_options['only'] = ('id', 'username')
        return self.parent.schema_dump_options(**schema_options)

    def schema_load_options(self, **schema_options):
        schema_options['only'] = ('id', 'username', 'is_active')
        return self.parent.schema_load_options(**schema_options)


class UserUpdateComponent(Component):

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
    jsonapi_type = 'users-emails'


class UserPhoneComponent(UserChildMixin, TypeComponent):
    model = UserPhoneModel
    schema = UserPhoneSchema
    jsonapi_type = 'users-phones'


class JSONAPIComponent(Component):
    """JSONAPI 1.0 Specification component.

    Documentation: https://jsonapi.org/
    """

    def make_query(self, query, **uri_args):
        """Count the number of results."""
        query = self.parent.make_query(query, **uri_args)
        self.count_query = query
        return query

    def deserialize(self, schema, request, **load_options):
        """Return flatened request set."""
        data = {}
        if 'data' not in request:
            raise ValueError('Invalid request data.')
        if 'id' not in request['data']:
            raise KeyError('Missing `id` field.')

        data['id'] = request['data']['id']
        for key, value in request['data'].get('attributes', {}).items():
            data[key] = value
        for key, value in request['data'].get('relationships', {}).items():
            data[key] = value.get('data')
        return self.parent.deserialize(schema, data, **load_options)

    def serialize(self, schema, model, **dump_options):
        """Return a formatted response."""
        def structure_contents(item):
            data = collections.defaultdict(dict)
            data['id'] = item.pop('id')
            data['type'] = self.parent.jsonapi_type
            for key, value in item.items():
                data['attributes'][key] = value
            return data

        response = self.parent.serialize(schema, model, **dump_options)
        metadata = {}

        if isinstance(response, list):
            response = [structure_contents(item) for item in response]
            metadata['meta'] = {'total': self.count_query.count()}
            metadata['links'] = {'self': request.base_url}
        else:
            response = structure_contents(response)

        response = {'data': response}
        response.update(metadata)
        return response
