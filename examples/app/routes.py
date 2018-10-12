# Construct some generic route types with default arguments.
from flask_router import Route
from functools import partial

from controllers import PlatformHandler, browse_type, get_type


Route = partial(Route, handler=PlatformHandler)
BrowseRoute = partial(Route, controller=browse_type, method='GET', path='')
GetRoute = partial(Route, controller=get_type, method='GET', path='/<id>')


# Construct the applications routes.
from flask_router import Include

from components import ActiveUserComponent, UserComponent, UserEmailComponent
from controllers import render_response


# User Routes
user = Include('', routes=[BrowseRoute(), GetRoute()], components=[UserComponent])

# User Child Routes
user_email = Include('/emails', routes=[BrowseRoute(), GetRoute()], components=[UserEmailComponent])

# Group user children.
user_subtypes = Include('/<user_id>', routes=[user_email])

# Group user types.
user_types = Include('/users', routes=[user, user_subtypes], components=[ActiveUserComponent])

# Construct a combined route with a middleware.
routes = []
routes.append(Include('', routes=[user_types], middleware=[render_response]))
