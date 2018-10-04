"""Basic flask_router usage.

To run this module please install flask and flask_router.
    `$ pip install flask`
    `$ pip install .`
"""
from flask import Flask
from flask_router import Component, Handler, Include, Route, Router


# Create some controller that takes a handler and does something useful
# with it.  A handler is the final, decoratored instance.  You should
# focus your effort on making these controllers as generic as possible.
#
# See "examples/efficient_usage.py" for additional implementation
# details.
def create_user(handler, **uri_args):
    user = handler.create()
    return str(user)


# Handlers.
class MyHandler(Handler):

    def create(self):
        return {'hello': 'world'}


# Components.
class A(Component):
    pass


class B(Component):
    
    def create(self):
        result = self.parent.create()
        result['B'] = True
        return result


# Route definition.
route = Include('/users', [
    Route('/<id>', create_user, handler=MyHandler, components=[B])],
    components=[A])


# Initialize your flask app.
app = Flask(__name__)


# Initialize the router with your app and add the routes.
api = Router(app)
api.add_routes([route])


# Confirm everything works.
with app.app_context():
    client = app.test_client()
    get = client.get('/users/1')
    print(get.data.decode('utf-8'))
