import unittest
import glm
from .rect import Rect


class TestCalculations(unittest.TestCase):

    def test_init_two_tuple(self):
        r = Rect((1, 2), (3, 4))
        self.assertEqual(r.left, 1 )
        self.assertEqual(r.top, 2 )
        self.assertEqual(r.right, 4 )
        self.assertEqual(r.bottom, 6 )
        self.assertEqual(r.width, 3 )
        self.assertEqual(r.height, 4 )
    def test_init_two_rect(self):
        r = Rect((1, 2), (3, 4))
        r2 = Rect(r)
        self.assertEqual(r2.left, 1 )
        self.assertEqual(r2.top, 2 )
        self.assertEqual(r2.right, 4 )
        self.assertEqual(r2.bottom, 6)
        self.assertEqual(r2.width, 3)
        self.assertEqual(r2.height, 4)
        self.assertEqual(r, r2)
    def test_init_two_vec2(self):
        r = Rect(glm.vec2(1, 2), glm.vec2(3, 4))
        self.assertEqual(r.left, 1 )
        self.assertEqual(r.top, 2 )
        self.assertEqual(r.right, 4 )
        self.assertEqual(r.bottom, 6)
        self.assertEqual(r.width, 3)
        self.assertEqual(r.height, 4)
    def test_init_four_float(self):
        r = Rect(1,2,3,4)
        self.assertEqual(r.left, 1 )
        self.assertEqual(r.top, 2 )
        self.assertEqual(r.right, 4 )
        self.assertEqual(r.bottom, 6)
        self.assertEqual(r.width, 3)
        self.assertEqual(r.height, 4)

    def test_topRight(self):
        r = Rect(1,2,3,4)
        self.assertEqual(r.topRight, (4,2) )
        self.assertIsInstance(r.topRight,glm.vec2)
    def test_topLeft(self):
        r = Rect(1,2,3,4)
        self.assertEqual(r.topLeft, (1,2) )
        self.assertIsInstance(r.topLeft,glm.vec2)
    def test_bottomLeft(self):
        r = Rect(1,2,3,4)
        self.assertEqual(r.bottomLeft, (1,6) )
        self.assertIsInstance(r.bottomLeft,glm.vec2)
    def test_bottomRight(self):
        r = Rect(1,2,3,4)
        self.assertEqual(r.bottomRight, (4,6) )
        self.assertIsInstance(r.bottomRight,glm.vec2)

    def test_center(self):
        r = Rect((1, 2), (4, 4))
        self.assertEqual(r.center, glm.vec2(3, 4) )
        r.center=(5,5)
        self.assertEqual(r.center, glm.vec2(5, 5) )
        self.assertEqual(r.topLeft, glm.vec2(3, 3) )
        r.center=glm.vec2(6,6)
        self.assertEqual(r.center, glm.vec2(6,6) )
        self.assertEqual(r.topLeft, glm.vec2(4, 4) )
        with self.assertRaises(Exception) as context:
            r.center="a"
        self.assertIsInstance(context.exception,ValueError)

    def test_inverse(self):
        r = Rect((1, 2), (4, 4))
        r.width = -4
        r.height = -6
        self.assertEqual(r.topLeft, glm.vec2(-3, -4) )
        self.assertEqual(r.size, glm.vec2(4, 6) )


if __name__ == "__main__":
    unittest.main()
