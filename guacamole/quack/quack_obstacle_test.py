import unittest
import glm
from guacamole.quack.quack_obstacle import QuackObstacle


class TestQuackBand(unittest.TestCase):

    def test_init_quackband(self):
        r = QuackObstacle(1, 2, 3)
        self.assertEqual(str(r), "QuackObstacle{position:2,type:1,size:3}")
        self.assertEqual(r.position, 2)
        self.assertEqual(r.type, 1)
        self.assertEqual(r.size, 3)

    def test_eq(self):
        r1 = QuackObstacle(1, 2, 3)
        r2 = QuackObstacle(1, 2, 3)
        r3 = QuackObstacle(2, 2, 3)
        self.assertEqual(r1, r2)
        self.assertNotEqual(r1, r3)
        self.assertNotEqual(r2, r3)


if __name__ == "__main__":
    unittest.main()
