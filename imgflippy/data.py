import inspect
import logging
from operator import itemgetter
from collections import OrderedDict

import requests
from six.moves.urllib.parse import unquote, urljoin

from imgflippy import Config
from imgflippy.model import validate_parameters

logger = logging.getLogger(__name__)


class Meme(object):

    def __init__(self, template, username, password, text0=None, text1=None,
                 font=None, max_font_size=None, boxes=None):

        self._template = template
        self._params = {'template_id': template.id}

        arg_info = inspect.getargvalues(inspect.currentframe())

        for k, v in arg_info.locals.items():
            if (v is None) or (isinstance(v, (self.__class__, MemeTemplate))):
                continue
            self._params.update({k: v})

        validate_parameters(self._params)
        logger.debug('Using parameters: {}'.format(self._params))

        self._request = requests.post(
            urljoin(Config.imgflip_api_url, 'caption_image'),
            params=self.parse_parameters(**self._params)
        )

        if not self._request.json().get('success'):
            raise LookupError(self._request.json().get('error_message'))

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.params == self.params

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self._template.name)

    @property
    def template(self):
        return self._template

    @property
    def params(self):
        return {k: v for k, v in self._params.items()
                if k not in ['username', 'password']}

    @property
    def url(self):
        return self._request.json().get('data', {}).get('url')

    @property
    def page_url(self):
        return self._request.json().get('data', {}).get('page_url')

    @staticmethod
    def parse_parameters(**kwargs):

        def _parse_list(list_):
            return {'[{}][{}]'.format(i, k_): v_
                    for i in range(len(list_))
                    for k_, v_ in list_[i].items()}

        result = OrderedDict()

        for k, v in kwargs.items():
            if isinstance(v, list):
                # I've had to update these one at a time so that the keys get
                # added in alphanumeric order, otherwise Python 2 butchers
                # things and the query gets messed up.
                for kp, vp in sorted(_parse_list(v).items(), key=itemgetter(0)):
                    result.update({unquote(''.join([k, kp])): vp})
            else:
                result.update({k: v})

        logger.debug('Parsed parameters: {}'.format(result))

        return result


class MemeTemplate(object):

    @classmethod
    def from_request_data(cls, data):
        return cls(**data)

    def __init__(self, id, name, url, width, height, box_count):
        self._id = id
        self._name = name
        self._url = url
        self._width = width
        self._height = height
        self._box_count = box_count

    def __eq__(self, other):
        return isinstance(other, self.__class__) and other.id == self.id

    def __hash__(self):
        return hash(self._id)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def url(self):
        return self._url

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def box_count(self):
        return self._box_count

    def add_caption(self, username, password, text0=None, text1=None,
                    font=None, max_font_size=None, boxes=None):

        return Meme(self, username, password, text0, text1, font,
                    max_font_size, boxes)
