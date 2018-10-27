## Flask Compose

A simple router that promotes component driven endpoint design.

#### Installation

```bash
$ pip install flask-compose
```

#### Getting Started

Please explore the "examples" directory for more detailed samples.

`flask-compose` can be applied to any `flask` application without consideration for any existing routing libraries.  `flask-compose`, at its core, is a glorified call to `Flask.add_url_rule`.

Creating a route is as simple as defining a few types:

```python
from flask import Flask
from flask_router import Component, Handler, Include, Route, Router


# Handler
class MyHandler(Handler): ...


# Components
class UserComponent(Component): ...
class SQLAlchemyComponent(Component): ...


# Controllers
def browse_type(handler, **uri_args): ...
def get_type(handler, **uri_args): ...


# Routes
route = Include(
    '/users', routes=[
        Route('', controller=browse_type, handler=MyHandler, components=[UserComponent]),
        Route('/<id>', controller=get_type, handler=MyHandler, components=[UserComponent]),
    ], components=[SQLAlchemyComponent])


app = Flask(__name__)
api = Router(app)
api.add_routes([route])
```

You're done!  The above code can be thought to evaluate to:

```python
# For browse type controllers.
def dispatch_request(**uri_args):
    handler = SQLAlchemyComponent(UserComponent(MyHandler()))
    return browse_type(handler, **uri_args)
```

#### Why

REST resources have well known behaviors that rarely deviate on a per resource basis.  Knowing this, resources should lend themselves to reuse.  However, as often happens in glue code, there is just enough variability between resources that reuse is either impossible or impractical.  The "Decorator Design Pattern" was concieved as an attempt to address this type of problem.  This library encourages its use through its routing system.

#### Philosophy

This library encourages the use of the "Decorator Design Pattern".  Not to be confused with Python's decorators, the "Decorator Design Pattern" is an object-oriented approach to annotating behavior.  The naming of these two concepts is not coincidental.  Python's decorators describe on a function-based level what the "Decorator Design Pattern" describes on an object-based level.

#### Credits

With thanks to the molten framework, flask, and "The Gang of Four" for their contributions to the software world.  Without whom this project would not have been possible.
