"""Basic flask_compose usage.

To run this module please install flask and flask_compose.
    `$ pip install flask`
    `$ pip install .`
"""
from flask import Flask
from flask_compose import Component, Handler, Include, Route, Router


# Create some controller that takes a handler and does something useful
# with it.  A handler is the final, decoratored instance.  You should
# focus your effort on making these controllers as generic as possible.
def create_user(handler, **uri_args):
    user = handler.create()
    return str(user)


# Create some "Handler" which implements the most generalized behavior
# of your application.
class MyHandler(Handler):

    def create(self):
        return {}


# Create some "Component" classes which decorate your application's
# behavior with more specialized business logic.
class A(Component):

    def create(self):
        result = self.parent.create()
        result['A'] = False
        return result


class B(Component):
    
    def create(self):
        result = self.parent.create()
        result['B'] = True
        return result


# Create a route structure which composes your components in some novel
# way.  The below code can be thought to evaluate to:
#
#   components = A(B(MyHandler()))
#   return create_user(components, **uri_args)
route = Route('/<id>', create_user, handler=MyHandler, components=[B])
route = Include('/users', routes=[route], components=[A])


# Initialize the router with your app and add the routes.
app = Flask(__name__)
api = Router(app)
api.add_routes([route])


with app.app_context():
    client = app.test_client()
    get = client.get('/users/1')  # {'A': False, 'B': True}
    print(get.data.decode('utf-8'))
