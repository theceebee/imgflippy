import logging
import math
import re

from six import string_types


logger = logging.getLogger(__name__)


class Parameters(object):

    class BoxesParameters(object):

        _name = 'boxes'

        text = 'text'
        x = 'x'
        y = 'y'
        width = 'width'
        height = 'height'
        color = 'color'
        outline_color = 'outline_color'

        def __eq__(self, other):
            return other == str(self)

        def __hash__(self):
            return hash(str(self))

        def __repr__(self):
            return self._name

        def __str__(self):
            return self._name

        @staticmethod
        def dimensions():
            return {Parameters.boxes.x,
                    Parameters.boxes.y,
                    Parameters.boxes.width,
                    Parameters.boxes.height}

        @staticmethod
        def colors():
            return {Parameters.boxes.color,
                    Parameters.boxes.outline_color}

    template_id = 'template_id'
    username = 'username'
    password = 'password'
    text0 = 'text0'
    text1 = 'text1'
    font = 'font'
    max_font_size = 'max_font_size'

    boxes = BoxesParameters()

    @staticmethod
    def required():
        return {Parameters.template_id,
                Parameters.username,
                Parameters.password}

    @staticmethod
    def text():
        return {Parameters.text0,
                Parameters.text1}


class Fonts(object):

    arial = 'arial'
    impact = 'impact'

    @staticmethod
    def valid():
        return [Fonts.arial,
                Fonts.impact]

    @staticmethod
    def default():
        return Fonts.impact


def validate_int(value, min_=0, max_=None):

    if not isinstance(value, int):
        try:
            value = int(value)
        except ValueError:
            return False

    if min_ is None:
        min_ = -math.inf

    if max_ is None:
        max_ = math.inf

    return min_ <= value <= max_


def validate_str(value, allow_empty=False):
    return isinstance(value, string_types) and (len(value) or allow_empty)


class ParameterException(BaseException):
    pass


class MissingParameterError(ParameterException):
    pass


class InvalidParameterError(ParameterException):
    pass


def validate_hex_color(value):
    if not re.match('#[0-9|A-F]{6}', value, re.I):
        raise InvalidParameterError(
            'Invalid value for color parameter: {}'.format(value))
    return True


def validate_boxes_parameter(list_):

    def validate_array_element(dict_):

        if Parameters.boxes.text not in dict_:
            raise MissingParameterError('No text parameter supplied.')

        if Parameters.boxes.dimensions().intersection(set(dict_)):

            if not Parameters.boxes.dimensions().issubset(set(dict_)):
                logger.warning('Be sure to specify all four dimension '
                               'parameters (x, y, width, height), otherwise '
                               'your text may not show up correctly.')

        # Validate color parameters.
        for color_param in Parameters.boxes.colors().intersection(set(dict_)):
            validate_hex_color(dict_[color_param])

    return all([validate_array_element(item) for item in list_])


def validate_parameters(dict_):

    for parameter in Parameters.required():

        if parameter not in dict_:
            raise MissingParameterError(parameter)

        if not validate_str(parameter):
            raise InvalidParameterError(parameter)

        # Check that the parameter values are non-empty string types.
        if not validate_str(dict_[parameter]):
            raise InvalidParameterError(parameter)

    if not (Parameters.text().intersection(set(dict_))
            or Parameters.boxes in dict_):

        raise MissingParameterError('No text parameter(s) supplied.')

    try:
        validate_boxes_parameter(dict_[Parameters.boxes])
    except KeyError:  # ie. there is no key 'boxes'.
        pass

    return True
