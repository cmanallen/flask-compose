from flask_router import Include, Route


# Consider a simple endpoint.
route = Include('/users', routes=[BrowseRoute(''), GetRoute('/<user_id>')])


# Now consider any number of nested endpoints.
#
# /users/1/emails
# /users/1/phones
#
# You can nest the routes. But this runs the risk of sharing components
# that are not wanted by the children.
route = Include('/users', routes=[
    BrowseRoute(''), Include('/<user_id>', routes=[
        GetRoute('', ignored_components=[UserChildren]),
        BrowseRoute('/emails', ignored_components=[UserSpecific]),
        BrowseRoute('/phones', ignored_components=[UserSpecific])
    ], components=[UserChildren])
], components=[UserSpecific])


# To solve this you can do one of two things.  Take the nesting even
# further or go back to a higher level of the tree.
#
# By nesting further we can reuse some of the routing structure. Empty
# "Include" types act as pass-throughs.
route = Include('/users', routes=[
    BrowseRoute(''), Include('/<user_id>', routes=[
        GetRoute(''), Include('', routes=[
            BrowseRoute('/emails'),
            BrowseRoute('/phones')
        ], components=[UserChildren], ignored_components=[UserSpecific])
    ])
], components=[UserSpecific])


# By flattening the tree we can create more legible code at the expense
# of duplication.
routes = []
routes.append(Include('/users', routes=[...], components=[UserSpecific]))
routes.append(Include('/users/<user_id>/emails', routes=[...], components=[UserChildren]))
routes.append(Include('/users/<user_id>/phones', routes=[...], components=[UserChildren]))
