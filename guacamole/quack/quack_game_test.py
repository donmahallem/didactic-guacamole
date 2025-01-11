import unittest
from .quack_game import QuackGame
from .quack_band import QuackBandType


class TestQuackScene(unittest.TestCase):

    def test_init_quackscene(self):
        r = QuackGame()

    def test_eq(self):
        r = QuackGame()
        r.resetGame(5)
        r2 = QuackGame()
        r2.resetGame(5)
        r3 = QuackGame()
        r3.resetGame(2)
        self.assertEqual(r.getBands(), r2.getBands())
        self.assertNotEqual(r.getBands(), r3.getBands())
        self.assertEqual(r.lastSeed, r2.lastSeed)
        self.assertNotEqual(r.lastSeed, r3.lastSeed)

    def test_reset(self):
        r = QuackGame()
        r.resetGame(29)
        bands = r.getBands()
        self.assertIsInstance(bands, dict)
        self.assertEqual(list(bands.keys()), list(range(13)))
        self.assertEqual(bands[0].type, QuackBandType.START)
        self.assertEqual(bands[1].type, QuackBandType.STREET)
        self.assertEqual(bands[2].type, QuackBandType.STREET)
        self.assertEqual(bands[3].type, QuackBandType.STREET)
        self.assertEqual(bands[4].type, QuackBandType.STREET)
        self.assertEqual(bands[5].type, QuackBandType.STREET)
        self.assertEqual(bands[6].type, QuackBandType.SAFE)
        self.assertEqual(bands[7].type, QuackBandType.WATER)
        self.assertEqual(bands[8].type, QuackBandType.WATER)
        self.assertEqual(bands[9].type, QuackBandType.WATER)
        self.assertEqual(bands[10].type, QuackBandType.WATER)
        self.assertEqual(bands[11].type, QuackBandType.WATER)
        self.assertEqual(bands[12].type, QuackBandType.END)


if __name__ == "__main__":
    unittest.main()
