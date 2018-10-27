from functools import partial
from unittest import TestCase

from flask_compose import Component, Include, Route, dispatch_request


class Handler: pass
class A(Component): pass
class B(Component): pass
class C(Component): pass


def controller(): return fn
def a_middleware(fn): return fn
def b_middleware(fn): return fn
def c_middleware(fn): return fn


class RouteTestCase(TestCase):

    def test_make_url_rule(self):
        """Test "make_url_rule" method."""
        outer_group = Include(
            '/users', routes=[], name='users_', components=[A],
            middleware=[a_middleware])
        inner_group = Include(
            '/emails', routes=[], name='emails_', components=[B],
            middleware=[b_middleware])
        route = Route(
            '/<id>', controller, Handler, 'GET', name='route', components=[C],
            ignored_components=[A], middleware=[c_middleware],
            ignored_middleware=[b_middleware])

        rule = route.make_url_rule([outer_group, inner_group])
        self.assertTrue(rule.methods == ['GET'])
        self.assertTrue(rule.path == '/users/emails/<id>')
        self.assertTrue(rule.name == 'users_emails_route')
        self.assertTrue(rule.components == [B, C])
        self.assertTrue(rule.middleware == [a_middleware, c_middleware])
        self.assertTrue(rule.controller == controller)
        self.assertTrue(rule.handler == Handler)

    def test_unnamed_make_url_rule(self):
        """Test "make_url_rule" method."""
        outer_group = Include('/users', routes=[])
        inner_group = Include('/emails', routes=[])
        route = Route('/<id>', None, None, 'GET')

        rule = route.make_url_rule([outer_group, inner_group])
        self.assertTrue(rule.methods == ['GET'])
        self.assertTrue(rule.path == '/users/emails/<id>')
        self.assertTrue(rule.name == '/users/emails/<id>GET')
