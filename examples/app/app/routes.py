"""Application routes definition.

Reading this module from bottom-to-top will add clarity to the
composition of the routes.
"""
from flask_compose import Include

from app.components import (
    ActiveUserComponent, UserComponent, UserEmailComponent, UserPhoneComponent,
    UserUpdateComponent, JSONAPIComponent)
from app.controllers import (
    BrowseRoute, CreateRoute, GetRoute, UpdateRoute, DeleteRoute)
from app.middleware import render_response


# User routes.
#
# Notice that we do not define a "/users" prefix to the URL.  We'll do
# this later on in our route definition scheme.
user_update = UpdateRoute(
    components=[UserUpdateComponent], ignored_components=[ActiveUserComponent])
user = Include('', routes=[
    BrowseRoute(), GetRoute(), CreateRoute(), user_update, DeleteRoute()],
    components=[UserComponent])


# User children routes.
user_email = Include('/emails', routes=[
    BrowseRoute(), GetRoute(), CreateRoute(), UpdateRoute(), DeleteRoute()],
    components=[UserEmailComponent])
user_phone = Include('/phones', routes=[
    BrowseRoute(), GetRoute(), CreateRoute(), UpdateRoute(), DeleteRoute()],
    components=[UserPhoneComponent])


# General "/<user_id>" path routes.
#
# The "user_child" include helps us define a common route structure.
# The above endpoints will now expect a "user_id" to be provided to
# their view functions.
user_child = Include('/<user_id>', routes=[user_email, user_phone])


# General "/users" path routes.
#
# We combine our children and our subtypes into a single include. Thanks
# to our component composition scheme, all of our routes on the
# "/users" path will require the user to be active.
user_types = Include(
    '/users', routes=[user, user_child], components=[ActiveUserComponent])


# Application routes.
#
# Finally, we reach the lowest level of our routing scheme. Here we
# specify some highly generalized components and middleware.  For
# demonstration purposes we'll create an unstructured endpoint and a
# JSONAPI formatted endpoint.
routes = []
routes.append(Include('/v1', routes=[user_types], middleware=[render_response]))
routes.append(Include(
    '/v2', routes=[user_types], components=[JSONAPIComponent],
    middleware=[render_response]))
