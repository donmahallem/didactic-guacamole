import unittest
import glm
from .animation import EaseInQuadAnimation


class TestAnimation(unittest.TestCase):

    def test_easeinquad(self):
        r = EaseInQuadAnimation(2)
        self.assertFalse(r.done)
        r.update(0.5)
        self.assertEqual(r.progress, 0.0625)

    def test_easeinquad_done(self):
        r = EaseInQuadAnimation(2)
        self.assertFalse(r.done)
        r.update(3)
        self.assertEqual(r.progress, 1)
        self.assertTrue(r.done)


if __name__ == "__main__":
    unittest.main()
