from typing import Any, Callable, Generator, List, Optional, Union, Tuple

import collections
import flask  # type: ignore
import functools


Components = Optional[List['Component']]
Middleware = Callable[[Callable[..., Any]], Callable[..., Any]]
Middlewares = Optional[List[Middleware]]
Routes = List['RouteLike']
IterRoute = Generator[Tuple[List['Include'], 'Route'], None, None]


Rule = collections.namedtuple('Rule', (
    'path', 'name', 'action', 'methods', 'controller', 'handler', 'components',
    'middleware'))


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

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, self.parent.__repr__())


class Handler:
    """Handler type.

    The "Concreate Class" in the decorator design pattern.  Handlers by
    default do nothing.  You must add your own functionality by
    subclassing this type.
    """

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)


def dispatch_request(
        fn: Callable, handler: Handler, components: List[Component],
        **uri_args: str):
    handler = handler()  # type: ignore
    for component in components:
        handler = component(handler)
    return fn(handler, **uri_args)


class RouteLike:

    def __init__(
            self,
            name: str = '',
            middleware: Middlewares = None,
            components: Components = None,
            ignored_middleware: Middlewares = None,
            ignored_components: Components = None) -> None:
        self.name = name
        self.middleware = middleware or []
        self.components = components or []
        self.ignored_middleware = ignored_middleware or []
        self.ignored_components = ignored_components or []


class Route(RouteLike):

    def __init__(
            self, path: str, controller: Callable, handler: Handler,
            method: str = 'GET', **route_opts) -> None:
        self.path = path
        self.controller = controller
        self.handler = handler
        self.method = method
        super().__init__(**route_opts)

    def make_url_rule(self, includes: List['Include']) -> Rule:
        """Return a "Rule" instance."""
        components: List[Component] = []
        middleware: List[Middleware] = []
        ignored_components: List[Component] = []
        ignored_middleware: List[Middleware] = []
        name = ''
        path = ''

        for include in includes:
            # Concatenate the components and middleware lists being
            # careful not to mutate the list.
            components = components + include.components
            middleware = middleware + include.middleware

            ignored_components = ignored_components + include.ignored_components
            ignored_middleware = ignored_middleware + include.ignored_middleware

            # Concatenate the names.
            name = '{}{}'.format(name, include.name)

            # Concatenate the paths.
            path = '{}{}'.format(path, include.path)

        # Concatenate components with the concrete class in last
        # place. Remove ignored items.
        ignored_components = ignored_components + self.ignored_components
        components = components + self.components
        components = [c for c in components if c not in ignored_components]

        # Concatenate middleware and remove ingnored items.
        ignored_middleware = ignored_middleware + self.ignored_middleware
        middleware = middleware + self.middleware
        middleware = [m for m in middleware if m not in ignored_middleware]

        # Set handler value.
        handler = self.handler

        # Construct the URI path.
        path = '{}{}'.format(path, self.path)

        # Construct a name for the route or default to the path.
        name = '{}{}'.format(name, self.name)
        if not name:
            name = path + self.method

        # Construct a function with the components pre-specified.
        view = dispatch_request
        view = functools.partial(
            view, fn=self.controller, handler=handler,
            components=list(reversed(components)))

        # Wrap the view with middleware. The first middleware in the
        # list is the last middleware applied.
        for middleware_ in reversed(middleware):
            view = middleware_(view)

        return Rule(
            path=path, name=name, action=view, methods=[self.method],
            controller=self.controller, handler=handler,
            components=components, middleware=middleware)


class Include(RouteLike):

    def __init__(self, path: str, routes: Routes, **route_opts) -> None:
        self.path = path
        self.routes = routes
        super().__init__(**route_opts)

    def __iter__(self) -> IterRoute:
        yield from self.iter_route_set([self])

    def iter_route_set(self, path: List['Include']) -> IterRoute:
        """Generate a tuple of ["Include"], "Route" pairs."""
        for route in self.routes:
            if isinstance(route, Route):
                yield path, route
            elif isinstance(route, Include):
                yield from route.iter_route_set(path + [route])


class Router:

    def __init__(self, app: flask.Flask) -> None:
        self.app = app
        self.rules: dict = {}

    def __iter__(self) -> Generator[str, None, None]:
        yield from self.rules

    def __getitem__(self, key: str) -> Rule:
        return self.rules[key]

    def __contains__(self, key: str) -> bool:
        return key in self.rules

    def __len__(self) -> int:
        return len(self.rules)

    def add_routes(self, items: Routes) -> None:
        """For each item add a URL rule to the application."""
        for item in items:
            if isinstance(item, Include):
                for includes, route in item:
                    self.add_route(includes, route)
            elif isinstance(item, Route):
                self.add_route([], item)

    def add_route(self, includes: List[Include], route: Route) -> None:
        """Create and add a URL rule to the application."""
        self.add_rule(route.make_url_rule(includes))

    def add_rule(self, rule: Rule) -> None:
        """Add a URL rule to the application."""
        self.rules[rule.name] = rule
        self.app.add_url_rule(
            rule.path, rule.name, rule.action, methods=rule.methods)

    def items(self) -> Generator[Tuple[str, Rule], None, None]:
        """Generate a tuple of key, value pairs."""
        yield from self.rules.items()
