from unittest import TestCase

from flask_compose import Include, Route


class IncludeTestCase(TestCase):

    def test_iter_include(self):
        """Test iterate "Include" type."""
        inner_route = Route('', None, None, '')
        outer_route = Route('', None, None, '')

        inner_group = Include('', routes=[inner_route])
        outer_group = Include('', routes=[inner_group, outer_route])

        iterator = iter(outer_group)

        groups, route = next(iterator)
        self.assertTrue(groups[0] == outer_group)
        self.assertTrue(groups[1] == inner_group)
        self.assertTrue(route == inner_route)

        groups, route = next(iterator)
        self.assertTrue(groups[0] == outer_group)
        self.assertTrue(route == outer_route)
