# Construct some generic route types with default arguments.
from flask_router import Route
from functools import partial

from controllers import (
    PlatformHandler, browse_type, get_type, create_type, update_type,
    delete_type)


Route = partial(Route, handler=PlatformHandler)
BrowseRoute = partial(Route, controller=browse_type, method='GET', path='')
CreateRoute = partial(Route, controller=create_type, method='POST', path='')
GetRoute = partial(Route, controller=get_type, method='GET', path='/<id>')
UpdateRoute = partial(Route, controller=update_type, method='PATCH', path='/<id>')
DeleteRoute = partial(Route, controller=delete_type, method='DELETE', path='/<id>')


# Construct the applications routes.
from flask_router import Include

from components import (
    ActiveUserComponent, UserComponent, UserEmailComponent, UserPhoneComponent,
    UserUpdateComponent)
from controllers import render_response


# User Routes
user = Include('', routes=[
    BrowseRoute(), GetRoute(), CreateRoute(), UpdateRoute(
        components=[UserUpdateComponent],
        ignored_components=[ActiveUserComponent]),
    DeleteRoute()], components=[UserComponent])

# User Child Routes
user_email = Include('/emails', routes=[
    BrowseRoute(), GetRoute(), CreateRoute(), UpdateRoute(), DeleteRoute()],
    components=[UserEmailComponent])
user_phone = Include('/phones', routes=[
    BrowseRoute(), GetRoute(), CreateRoute(), UpdateRoute(), DeleteRoute()],
    components=[UserPhoneComponent])

# Group user children.
user_subtypes = Include('/<user_id>', routes=[user_email, user_phone])

# Group user types.
user_types = Include('/users', routes=[user, user_subtypes], components=[ActiveUserComponent])

# Construct a combined route with a middleware.
routes = []
routes.append(Include('', routes=[user_types], middleware=[render_response]))
