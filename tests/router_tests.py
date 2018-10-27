from unittest import TestCase

from flask import Flask
from flask_compose import Include, Route, Router, Rule


class Handler: pass


def controller(handler, **uri_args): return '', 200


class RouterTestCase(TestCase):

    def test_router_add_routes(self):
        """Test "add_routes" method."""
        app = Flask('test')
        router = Router(app)

        route = Route('/<id>', controller, Handler, 'GET', name='instance')
        group = Include('/users', name='user_', routes=[route])

        router.add_routes([group])
        self.assertTrue('user_instance' in router)
        self.assertTrue(isinstance(router['user_instance'], Rule))

        router.add_routes([route])
        self.assertTrue('instance' in router)
        self.assertTrue(isinstance(router['instance'], Rule))

        with app.app_context():
            client = app.test_client()

            get = client.get('/users/1')
            self.assertTrue(get.status_code == 200)

            get = client.get('/1')
            self.assertTrue(get.status_code == 200)

    def test_router_dict(self):
        """Test iterate "Include" type."""
        router = Router(None)
        router.rules = {'a': 1, 'b': 2}

        # Assert __contains__.
        self.assertTrue('a' in router)
        self.assertTrue('c' not in router)

        # Assert __len__.
        self.assertTrue(len(router) == 2)

        # Assert __getitem__.
        self.assertTrue(router['a'] == 1)

        # Assert __iter__.
        iterator = iter(router)
        self.assertTrue(next(iterator) == 'a')
        self.assertTrue(next(iterator) == 'b')

        # Assert items.
        iterator = router.items()
        self.assertTrue(next(iterator) == ('a', 1))
        self.assertTrue(next(iterator) == ('b', 2))
