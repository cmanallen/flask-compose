from typing import Any, Callable, List, Optional, Union

import collections
import flask
import functools


Components = Optional[List['Component']]
Middleware = Callable[[Callable[..., Any]], Callable[..., Any]]
Middlewares = Optional[List[Middleware]]
Parent = Union['Component', 'Handler']
RouteLike = Union['Route', 'Include']
Routes = Optional[List[RouteLike]]


Rule = collections.namedtuple('Rule', ('path', 'name', 'action', 'methods'))


class Component:
    """Component type.

    The "Decorator Class" in the decorator design pattern.  Decorator
    classes are called "components" to avoid confusion with python
    @decorators.

    If a component does not implement any of the methods of the
    concrete class it will act as a pass-through.
    """

    def __init__(self, parent: Any) -> None:
        self.parent = parent

    def __getattr__(self, name: str) -> Any:
        return getattr(self.parent, name)


class Handler:
    """Handler type.

    The "Concreate Class" in the decorator design pattern.  Handlers by
    default do nothing.  You must add your own functionality by
    subclassing this type.
    """

    pass


def dispatch_request(fn: Callable, decorators: List[Parent], **uri_args: str):
    # Initialize the concrete class.  The concrete class will always
    # exist at the end of the list.
    handler = decorators.pop()
    handler = handler()

    # Initialize each of the remaining decorators being sure to
    # populate their __init__ with the previously initialized class.
    while decorators:
        decorator = decorators.pop()
        handler = decorator(handler)

    # Pass the handler instance into our controller function and return
    # its result.
    return fn(handler, **uri_args)


class Route:

    def __init__(
            self,
            path: str,
            controller: Callable,
            handler: Handler,
            method: str = 'GET',
            name: str = '',
            middleware: Middlewares = None,
            components: Components = None) -> None:
        self.path = path
        self.controller = controller
        self.handler = handler
        self.method = method
        self.name = name
        self.middleware = middleware or []
        self.components = components or []

    def make_url_rule(self, includes: List['Include']) -> Rule:
        """Return a "Rule" instance."""
        components: List[Any] = []
        middleware: List[Middleware] = []
        name = ''
        path = ''

        for include in includes:
            # Concatenate the components and middleware lists being
            # careful not to mutate the list.
            components = components + include.components
            middleware = middleware + include.middleware

            # Concatenate the names.
            name = '{}{}'.format(name, include.name)

            # Concatenate the paths.
            path = '{}{}'.format(path, include.path)

        # Concatenate components with the concrete class in last
        # place.
        components = components + self.components + [self.handler]

        # Construct the URI path.
        path = '{}{}'.format(path, self.path)

        # Construct a name for the route or default to the path.
        name = '{}{}'.format(name, self.name)
        if not name:
            name = path + self.method

        # Construct a function with the components pre-specified.
        view = dispatch_request
        view = functools.partial(view, fn=self.controller, decorators=components)

        # Wrap the view with middleware. The first middleware in the
        # list is the last middleware applied.
        middleware = middleware + self.middleware
        while middleware:
            wrap = middleware.pop()
            view = wrap(view)

        return Rule(path, name, view, [self.method])


class Include:

    def __init__(
            self,
            path: str,
            routes: Routes,
            name: str = '',
            middleware: Middlewares = None,
            components: Components = None) -> None:
        self.path = path
        self.routes = routes
        self.name = name
        self.middleware = middleware or []
        self.components = components or []


class Router:

    def __init__(self, app: flask.Flask) -> None:
        self.app = app

    def add_routes(
            self, routes: Routes,
            includes: Optional[List[Include]] = None) -> None:
        """For each route add a URL rule to the application."""
        includes = includes or []
        for route in routes:
            self.add_route(route, includes)

    def add_route(self, route: RouteLike, includes: List[Include]) -> None:
        """Add a URL rule to the application."""
        if isinstance(route, Include):
            # Append the include and recurse deeper into the tree.
            self.add_routes(route.routes, includes + [route])
        elif isinstance(route, Route):
            # Create a URL Rule instance.
            rule = route.make_url_rule(includes)

            # Add the URL rule to the application.
            self.app.add_url_rule(
                rule.path, rule.name, rule.action, methods=rule.methods)
