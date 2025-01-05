import unittest
import glm
from .rect import Rect


class TestCalculations(unittest.TestCase):

    def test_init(self):
        r = Rect((1, 2), (3, 4))
        self.assertEqual(r.left, 1, "The sum is wrong.")
        self.assertEqual(r.top, 2, "The sum is wrong.")
        self.assertEqual(r.width, 3, "The sum is wrong.")
        self.assertEqual(r.height, 4, "The sum is wrong.")

    def test_center(self):
        r = Rect((1, 2), (4, 4))
        self.assertEqual(r.center, glm.vec2(3, 4), "The sum is wrong.")

    def test_inverse(self):
        r = Rect((1, 2), (4, 4))
        r.width = -4
        r.height = -6
        self.assertEqual(r.topLeft, glm.vec2(-3, -4), "The sum is wrong.")
        self.assertEqual(r.size, glm.vec2(4, 6), "The sum is wrong.")


if __name__ == "__main__":
    unittest.main()
