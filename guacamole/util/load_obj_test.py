import unittest
import glm
from guacamole.util.load_obj import loadObj


class TestLoadObjFile(unittest.TestCase):

    def test_init_two_tuple(self):
        r = loadObj("./guacamole/util/box.obj")
        self.assertIsInstance(r, list)
        self.assertEqual(len(r), 288)


if __name__ == "__main__":
    unittest.main()
