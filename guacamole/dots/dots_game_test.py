import unittest
import numpy as np
from .dots_game import DotsGame


class TestDotsGame(unittest.TestCase):

    def test_init_dotsgame(self):
        r = DotsGame()

    def test_reset(self):
        r1 = DotsGame()
        r2 = DotsGame()
        r3 = DotsGame()
        r1.reset(1)
        r2.reset(1)
        r3.reset(2)
        self.assertEqual(r1, r2)
        self.assertNotEqual(r1, r3)

    def test_field(self):
        r = DotsGame()
        testField = [[1, 1, 1], [1, 0, 1], [3, 1, 1]]
        r.field = testField
        self.assertListEqual(
            sorted(r.selectConnected(0, 0)),
            sorted([(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 1), (2, 2)]),
        )
        self.assertIsNone(r.selectConnected(1, 1))

    def test_field_selectDots(self):
        r = DotsGame()
        testField = [[2, 2, 2], [1, 0, 1], [1, 1, 1], [1, 2, 1]]
        r.field = testField
        connected = r.selectConnected(0, 0)
        self.assertEqual(len(connected), 3)
        moved = r.selectDots(connected)
        np.testing.assert_equal(r.field, [[1, 1, 1], [1, 2, 1], [1, 0, 1], [0, 0, 0]])
        self.assertEqual(moved[0], len(connected))
        self.assertSetEqual(
            moved[1],
            set(
                [
                    ((1, 0), (0, 0), 1),
                    ((2, 0), (1, 0), 1),
                    ((3, 0), (2, 0), 1),
                    ((3, 1), (1, 1), 2),
                    ((1, 2), (0, 2), 1),
                    ((2, 1), (0, 1), 1),
                    ((3, 2), (2, 2), 1),
                    ((2, 2), (1, 2), 1),
                ]
            ),
        )
        self.assertEqual(r.score, 6)

    def test_applyGravity_no_change(self):
        r = DotsGame()
        testField = [[2, 2, 2], [1, 0, 1], [0, 0, 0], [0, 0, 0]]
        r.field = testField
        moved = r.applyGravity()
        np.testing.assert_equal(r.field, testField)
        self.assertIsNone(moved)

    def test_applyGravity_vertical(self):
        r = DotsGame()
        testField2 = [[2, 2, 2], [1, 0, 1], [0, 0, 0], [1, 2, 3]]
        r.field = testField2
        moved = r.applyGravity()
        np.testing.assert_equal(r.field, [[2, 2, 2], [1, 2, 1], [1, 0, 3], [0, 0, 0]])
        self.assertSetEqual(
            moved, set([((3, 0), (2, 0), 1), ((3, 1), (1, 1), 2), ((3, 2), (2, 2), 3)])
        )

    def test_applyGravity_horizontal(self):
        r = DotsGame()
        testField3 = [[2, 0, 2], [1, 0, 3], [1, 0, 0]]
        r.field = testField3
        moved = r.applyGravity()
        np.testing.assert_equal(r.field, [[2, 2, 0], [1, 3, 0], [1, 0, 0]])
        self.assertSetEqual(moved, set([((0, 2), (0, 1), 2), ((1, 2), (1, 1), 3)]))

    def test_applyGravity_diagonal_simple(self):
        r = DotsGame()
        testField3 = [[2, 0, 2], [1, 0, 0], [0, 0, 0], [1, 0, 3]]
        r.field = testField3
        moved = r.applyGravity()
        np.testing.assert_equal(r.field, [[2, 2, 0], [1, 3, 0], [1, 0, 0], [0, 0, 0]])
        self.assertSetEqual(
            moved, set([((0, 2), (0, 1), 2), ((3, 2), (1, 1), 3), ((3, 0), (2, 0), 1)])
        )

    def test_applyGravity_diagonal_space_tile_space(self):
        r = DotsGame()
        testField3 = [[2, 0, 2, 0, 3], [1, 0, 0, 0, 0], [0, 0, 0, 0, 4]]
        r.field = testField3
        moved = r.applyGravity()
        np.testing.assert_equal(
            r.field, [[2, 2, 3, 0, 0], [1, 0, 4, 0, 0], [0, 0, 0, 0, 0]]
        )
        self.assertSetEqual(
            moved, set([((0, 4), (0, 2), 3), ((0, 2), (0, 1), 2), ((2, 4), (1, 2), 4)])
        )

    def test_isFinished(self):
        r = DotsGame()
        testField = [[2, 1, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        r.field = testField
        self.assertTrue(r.isFinished(), "Game has no moves left")
        r.field = [[2, 1, 0], [2, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.assertFalse(r.isFinished(), "Game is has moves left")

    def test_get_attribute(self):
        r = DotsGame()
        testField = [[2, 2, 2], [1, 0, 1], [1, 1, 1], [1, 2, 1]]
        r.field = testField
        for y in range(4):
            for x in range(3):
                self.assertEqual(
                    r[(y, x)], testField[y][x], f"({y},{x}) is missmatching"
                )


if __name__ == "__main__":
    unittest.main()
