"""Efficient flask_router usage.

To run this module please install flask and flask_router.
    `$ pip install flask`
    `$ pip install .`
"""
from flask import g
from flask_router import Component, Handler


# Your concrete "handler" class.
#
# This class should define all of the behavior you wish to decorator
# within your controller. When in doubt decorate!


class PlatformHandler(Handler):

    def model_response(self, models, serializer) -> dict:
        if not isinstance(models, list):
            models = [models]
        return serializer.dump(models)

    def query_response(self, query, serializer) -> dict:
        models = query.all()
        return serializer.dump(models)

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


# Your decorator (named "component" for clarity) class.
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
        return query.filter(model.is_active.is_(True))

    def resolve_serializer(self):
        return UserSchema

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


# /controllers.py
def browse(handler, **uri_args):
    pass


def get(handler, **uri_args):
    pass


def create(handler, **uri_args):
    pass


def update(handler, **uri_args):
    pass


def delete(handler, **uri_args):
    pass


# /routes.py
routes = []


# /factory.py
app = Flask(__name__)

api = Router(app)
api.add_routes(routes)
