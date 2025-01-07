import unittest
import glm
from .sprite import Sprite
from .group import Group


class TestGroup(unittest.TestCase):

    def test_init(self):
        r = Group()

    def test_add_child(self):
        r = Group()
        s = Sprite()
        r.add(s)
        self.assertEqual(len(r), 1)

    def test_iadd_child(self):
        r = Group()
        s = Sprite()
        r += s
        self.assertEqual(len(r), 1)

    def test_isub_child(self):
        r = Group()
        s = Sprite()
        r += s
        self.assertEqual(len(r), 1)
        r -= s
        self.assertEqual(len(r), 0)

    def test_contains_child(self):
        r = Group()
        s = Sprite()
        r += s
        self.assertTrue(s in r)


if __name__ == "__main__":
    unittest.main()
