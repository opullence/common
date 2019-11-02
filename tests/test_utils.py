import unittest

from opulence.common.utils import is_list


class TestIsList(unittest.TestCase):
    def test_simple_list(self):
        lists = [(1, 2, 3), [4, 5, 6], {7, 8, 9}]
        for l in lists:
            self.assertEqual(is_list(l), True)

    def test_simple_non_lists(self):
        class toto:
            pass

        non_lists = [1, 2, "hello", 0.42, toto(), u"nicode"]
        for l in non_lists:
            self.assertEqual(is_list(l), False)
