from unittest import TestCase

from flask_router import Component, dispatch_request


class Handler:
    type = 'handler'

    def test(self):
        return ''


class A(Component): type = 'A'
class B(Component): type = 'B'


class TypeTestCase(TestCase):

    def test_component(self):
        """Test "Component" class."""
        handler = Component(Handler())
        self.assertTrue(handler.test() == '')
        self.assertTrue(hasattr(Component, 'test') is False)
        self.assertTrue(hasattr(handler, 'test'))

    def test_dispatch_request(self):
        """Test "dispatch_request" function."""
        def controller(handler, **uri_args):
            # Assert handler nesting.
            self.assertTrue(isinstance(handler, Component))
            self.assertTrue(isinstance(handler.parent, Component))
            self.assertTrue(isinstance(handler.parent.parent, Handler))

            # Assert component ordering.
            self.assertTrue(handler.type == 'A')
            self.assertTrue(handler.parent.type == 'B')
            self.assertTrue(handler.parent.parent.type == 'handler')

            # Assert uri_args passed.
            self.assertTrue(len(uri_args) == 2)
            self.assertTrue(uri_args['a'] == 1)
            self.assertTrue(uri_args['b'] == 2)

        dispatch_request(controller, Handler, [A, B], a=1, b=2)
