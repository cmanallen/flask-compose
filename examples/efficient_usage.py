"""Efficient flask_router usage.

To run this module please install flask and flask_router.
    `$ pip install flask`
    `$ pip install .`
"""
from flask import Flask
from flask_router import Component, Handler, Include, Route, Router

import functools


# Typical data types in most projects.


class UserModel:
    query = [1, 2, 3]


class UserSerializer:

    def __init__(self, *args, **kwargs): pass

    def dump(self, models):
        return [str(model) for model in models]


# Your concrete "handler" class.
#
# This class should define all of the behavior you wish to decorate
# within your controller.


class PlatformHandler(Handler):

    def model_response(self, models, serializer) -> dict:
        if not isinstance(models, list):
            models = [models]
        return serializer.dump(models)

    def query_response(self, query, serializer) -> dict:
        return self.model_response(query, serializer)

    def resolve_model(self):
        raise NotImplementedError

    def resolve_query(self, model):
        return model.query

    def resolve_serializer(self):
        raise NotImplementedError

    def resolve_serializer_options(self):
        return {}

    def resolve_load_options(self):
        return {}

    def resolve_dump_options(self):
        return {}


# Your decorator class (named "component" for clarity).
#
# It is not necessary to define a base decorator class. The "Component"
# class will automatically implement all of the behaviors of the
# handler class.


class UserComponent(Component):
    """A low level component for defining basic resource type meta.
    
    Notice this component does not call it's parent.  It is useful in
    some situations to terminate prematurely.  Because this component
    is not generic in nature and must return a specific type to be
    useful there is no need to proceed further down the chain.

    In general, the more specific the component the lower level it
    should be.  In the reciprocal, the more generic the component the
    closer to the outer-shell of the application it should be.
    """

    def resolve_model(self):
        return UserModel

    def resolve_query(self, model):
        query = self.parent.resolve_query(model)
        # If it were real.
        # return query.filter(model.is_active.is_(True))
        return query

    def resolve_serializer(self):
        return UserSerializer

    def resolve_serializer_options(self):
        result = self.parent.resolve_serializer_options()
        result.update({'only': ('id', 'username')})
        return result


class PatchComponent(Component):
    """A higher level component for defining generic serializer args.

    Two items of note:

    The first, should we have set the 'partial' key here? If all update
    operations implement this should we have implemented it as a
    behavior of the "update" controller above?

    The second, how do we retrieve the "self.model_instance" attribute?
    Components allow us to traverse _down_ to the core of the
    application but crucially do not allow us to take attributes from
    wrappers _higher_ up in the decorator chain.  Because of this we
    must take extra care with our decorator ordering.

    Consider the first point again. Should "model_instance" exist here?
    Perhaps this option is better set in the controller.  The more
    generalized a component becomes the more it lends itself to being
    handled within the controller. Ultimately, the variance in behavior
    (or lack thereof) will make the decision for you.

    In this case, I will always want to set partial and I will always
    want to set the context.  Because of this we should move this
    behavior into the controller.
    """

    def resolve_load_options(self):
        result = self.parent.resolve_load_options()
        result.update({'partial': True, 'context': self.model_instance})
        return result


# "/controllers.py"
def browse(handler, **uri_args):
    model_cls = handler.resolve_model()
    query = handler.resolve_query(model_cls)

    serializer_cls = handler.resolve_serializer()
    serializer = serializer_cls(handler.resolve_serializer_options())

    response = handler.query_response(query, serializer)
    return str(response), 200


def get(handler, **uri_args):
    pass


def create(handler, **uri_args):
    pass


def update(handler, **uri_args):
    pass


def delete(handler, **uri_args):
    pass


# "/routes.py"

# Define a generic application route. The handler should be generalized.
MyRoute = functools.partial(Route, handler=PlatformHandler)

# Define generic request method routes.  The controllers should be
# generalized and not require frequent changes.
MyBrowseRoute = functools.partial(MyRoute, controller=browse, method='GET')
MyGetRoute = functools.partial(MyRoute, controller=get, method='GET')
MyCreateRoute = functools.partial(MyRoute, controller=create, method='POST')
MyUpdateRoute = functools.partial(MyRoute, controller=update, method='PATCH')
MyDeleteRoute = functools.partial(MyRoute, controller=delete, method='DELETE')


# Create your route structure. If you choose to name the parent
# structure be sure to name the routes themselves!
routes = []
routes.append(
    Include('/users', components=[UserComponent], routes=[
        MyBrowseRoute(''), MyCreateRoute(''), MyGetRoute('/<id>'),
        MyUpdateRoute('/<id>'), MyDeleteRoute('/<id>')]
    )
)


# "/factory.py"
app = Flask(__name__)

api = Router(app)
api.add_routes(routes)

with app.app_context():
    print(app.test_client().get('/users').data.decode('utf-8'))
