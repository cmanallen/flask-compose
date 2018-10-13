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

    def schema_dump_options(self, **schema_options):
        """Return schema dump options."""
        return schema_options

    def schema_load_options(self, **schema_options):
        """Return schema load options."""
        return schema_options

    def fetch_all(self, query):
        """Return a collection of resources."""
        return query.all()

    def fetch_one(self, query):
        """Return a resource."""
        return query.first()

    def make_query(self, query, **uri_args):
        return query

    def deserialize(self, schema, data, **load_options):
        return schema.load(data, **load_options)

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
    schema = schema(**handler.schema_dump_options())

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
    schema = schema(**handler.schema_dump_options())

    result = handler.serialize(schema, model)
    return result, 200


def create_type(handler, **uri_args):
    """Create and return a resource.

    Steps:
        1. Deserialize the request data.
        2. Create a new resource.
        3. Construct a serializer.
        4. Return a serailized response.
    """
    form = request.data.decode('utf-8')
    form = json.loads(form)

    schema = handler.schema
    schema = schema(**handler.schema_load_options())
    result, errors = handler.deserialize(schema, form)
    if errors:
        return errors, 401

    model = handler.model(**result)
    db.session.add(model)
    db.session.commit()

    schema = handler.schema
    schema = schema(**handler.schema_dump_options())

    result = handler.serialize(schema, model)
    return result, 201


def update_type(handler, **uri_args):
    """Update and return a requested resource.

    Steps:
        1. Construct a query.
        2. Fetch the requested resource.
        3. Abort if a resource is not found.
        4. Deserialize the request data.
        5. Update the resource.
        6. Construct a serializer.
        7. Return a serailized response.
    """
    query = handler.query
    query = handler.make_query(query, **uri_args)
    model = handler.fetch_one(query)
    if not model:
        abort(404)

    form = request.data.decode('utf-8')
    form = json.loads(form)

    schema = handler.schema
    schema = schema(**handler.schema_load_options())
    result, errors = handler.deserialize(schema, form, partial=True)
    if errors:
        return errors, 401

    for key, value in result.items():
        setattr(model, key, value)
    db.session.add(model)
    db.session.commit()

    schema = handler.schema
    schema = schema(**handler.schema_dump_options())

    result = handler.serialize(schema, model)
    return result, 202


def delete_type(handler, **uri_args):
    """Delete a resource and return an empty content response.

    Steps:
        1. Construct a query.
        2. Fetch the requested resource.
        3. Abort if a resource is not found.
        4. Delete the resource.
        5. Return an empty response.
    """
    query = handler.query
    query = handler.make_query(query, **uri_args)
    model = handler.fetch_one(query)
    if not model:
        abort(404)

    db.session.delete(model)
    db.session.commit()

    return '', 204
