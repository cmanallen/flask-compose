from components import (
    ActiveUserComponent, UserComponent, UserEmailComponent, UserPhoneComponent,
    UserUpdateComponent)
from controllers import (
    BrowseRoute, CreateRoute, GetRoute, UpdateRoute, DeleteRoute)
from flask_router import Include
from middleware import render_response


# User routes.
#
# You can define your routes separately and then throw them into a
# shared group.
user_update = UpdateRoute(
    components=[UserUpdateComponent], ignored_components=[ActiveUserComponent])
user = Include('', routes=[
    BrowseRoute(), GetRoute(), CreateRoute(), user_update, DeleteRoute()],
    components=[UserComponent])


# User children routes.
#
# You can also define the routes inline. Functionally, there is no
# difference. What matters is developer productivity.
#
# The "user_child" include helps us define a common route structure.
# The above endpoints will now expect a "user_id" to be provided to
# their view functions.
user_email = Include('/emails', routes=[
    BrowseRoute(), GetRoute(), CreateRoute(), UpdateRoute(), DeleteRoute()],
    components=[UserEmailComponent])
user_phone = Include('/phones', routes=[
    BrowseRoute(), GetRoute(), CreateRoute(), UpdateRoute(), DeleteRoute()],
    components=[UserPhoneComponent])
user_child = Include('/<user_id>', routes=[user_email, user_phone])


# General "/users" path routes.
#
# We combine our children and our subtypes into a single route. Thanks
# to our component composition scheme, all of our routes on the
# "/users" path will require the user to be active.
user_types = Include(
    '/users', routes=[user, user_child], components=[ActiveUserComponent])


# Application routes.
#
# Finally, we reach the final level of our routing scheme. Here we
# specify some highly generalized components and middleware.
routes = []
routes.append(Include('', routes=[user_types], middleware=[render_response]))
