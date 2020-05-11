import itertools
import unittest

from six import string_types

from pyimgflip import model


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


    # def test_typing(self):
    # #     v = model.Primative(type_=(int, string_types))
    # #     self.assertTrue(v.validate(1))
    # #     self.assertTrue(v.validate('1'))
    # #
    # # def test_func(self):
    # #     v = model.Primative(type_=(int, string_types), func=lambda x: int(x) > 0)
    # #     self.assertTrue(v.validate(1))
    # #     self.assertTrue(v.validate('1'))
    # #     self.assertRaises(AssertionError, v.validate, 0)
    # #     self.assertRaises(AssertionError, v.validate, '0')


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
