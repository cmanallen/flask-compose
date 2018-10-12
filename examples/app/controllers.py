from flask import abort, jsonify, make_response, request
from flask_router import Handler

from common import db

import json


def render_response(fn):
    def decorator(*args, **kwargs):
        data, code = fn(*args, **kwargs)
        return make_response(jsonify(data), code)
    return decorator


class PlatformHandler(Handler):

    @property
    def model(self):
        raise NotImplementedError

    @property
    def schema(self):
        raise NotImplementedError

    @property
    def schema_dump_options(self):
        return {}

    @property
    def schema_load_options(self):
        return {}

    def fetch_all(self, query):
        """Return a collection of resources."""
        return query.all()

    def fetch_one(self, query):
        """Return a resource."""
        return query.first()

    def make_query(self, query, **uri_args):
        return query

    def serialize(self, schema, model):
        return schema.dump(model).data

    def serialize_all(self, schema, models):
        return [self.serialize(schema, model) for model in models]


def browse_type(handler, **uri_args):
    """Return a collection endpoint response.

    Steps:
        1. Construct a query.
        2. Construct a serializer.
        3. Fetch all of the resources.
        4. Return a serailized response.
    """
    query = handler.query
    query = handler.make_query(query, **uri_args)

    schema = handler.schema
    schema = schema(**handler.schema_dump_options)

    models = handler.fetch_all(query)
    result = handler.serialize_all(schema, models)
    return result, 200


def get_type(handler, **uri_args):
    """Return an instance endpoint response.

    Steps:
        1. Construct a query.
        2. Fetch the requested resource.
        3. Abort if a resource is not found.
        4. Construct a serializer.
        5. Return a serailized response.
    """
    query = handler.query
    query = handler.make_query(query, **uri_args)
    model = handler.fetch_one(query)
    if not model:
        abort(404)

    schema = handler.schema
    schema = schema(**handler.schema_dump_options)

    result = handler.serialize(schema, model)
    return result, 200


# def create_type(handler, **uri_args):
#     return response, 201


# def update_type(handler, **uri_args):
#     return response, 202


# def delete_type(handler, **uri_args):
#     return response, 204
