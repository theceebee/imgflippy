import itertools
import unittest

from imgflippy import model


class TestValidation(unittest.TestCase):

    def test_validate_int(self):
        self.assertTrue(model.validate_int(value=0, min_=0, max_=None))
        self.assertFalse(model.validate_int(value=-1, min_=0, max_=None))
        self.assertTrue(model.validate_int(value=0, min_=None, max_=0))
        self.assertFalse(model.validate_int(value=1, min_=None, max_=0))
        self.assertTrue(model.validate_int(value='0', min_=0, max_=None))
        self.assertFalse(model.validate_int(value='-1', min_=0, max_=None))
        self.assertTrue(model.validate_int(value='0', min_=None, max_=0))
        self.assertFalse(model.validate_int(value='1', min_=None, max_=0))

    def test_validate_str(self):
        self.assertTrue(model.validate_str('foo', allow_empty=True))
        self.assertTrue(model.validate_str('foo', allow_empty=False))
        self.assertTrue(model.validate_str('', allow_empty=True))
        self.assertFalse(model.validate_str('', allow_empty=False))


class TestParameterValidation(unittest.TestCase):

    @unittest.skip
    def test_validate_hex_color(self):

        def hex_color_from_rgb(r, g, b):
            return '#{:02X}{:02X}{:02X}'.format(r, g, b)

        all_colors = [hex_color_from_rgb(*perm)
                      for perm in itertools.permutations(range(255), 3)]

        self.assertTrue(all([model.validate_hex_color(color)
                             for color in all_colors]))


if __name__ == '__main__':
    unittest.main()
