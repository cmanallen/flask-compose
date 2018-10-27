from unittest import TestCase

from flask_compose import Component, dispatch_request


class Handler:
    type = 'handler'

    def test(self):
        return ''

    def leak(self):
        return None


class A(Component):
    type = 'A'

    def leak(self):
        self.am_i_leaking = False
        self.parent.leak()

    def check_val(self):
        return self.am_i_leaking == False


class B(Component):
    type = 'B'

    def leak(self):
        self.parent.leak()
        if hasattr(self, 'am_i_leaking'):
            raise Exception('I leaked.')



class TypeTestCase(TestCase):

    def test_component(self):
        """Test "Component" class."""
        handler = Component(Handler())
        self.assertTrue(handler.test() == '')
        self.assertTrue(hasattr(Component, 'test') is False)
        self.assertTrue(hasattr(handler, 'test'))

    def test_component_leaking(self):
        """Assert "Component" instance does not leak into other classes."""
        handler = A(B(Handler()))
        handler.leak()

        self.assertTrue(hasattr(handler, 'am_i_leaking'))
        self.assertTrue(not hasattr(handler.parent, 'am_i_leaking'))
        self.assertTrue(handler.check_val())

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

        dispatch_request(controller, Handler, [B, A], a=1, b=2)
