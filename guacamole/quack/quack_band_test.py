import unittest
import glm
from guacamole.quack.quack_band import QuackBand


class TestQuackBand(unittest.TestCase):

    def test_init_quackband(self):
        r = QuackBand(1, 2, 3, [])
        self.assertEqual(
            str(r), 'Quackband{id:"1",type:"2",initialOffset:"3",obstacles:[0]}'
        )
        self.assertEqual(r.id, 1)
        self.assertEqual(r.type, 2)
        self.assertEqual(r.initalOffset, 3)
        self.assertEqual(len(r.obstacles), 0)

    def test_eq(self):
        r1 = QuackBand(1, 2, 3, [4])
        r2 = QuackBand(1, 2, 3, [4])
        r3 = QuackBand(1, 2, 3, [5])
        self.assertEqual(r1, r2)
        self.assertNotEqual(r1, r3)
        self.assertNotEqual(r2, r3)


if __name__ == "__main__":
    unittest.main()
