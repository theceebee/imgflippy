import re

import requests
from six.moves.urllib.parse import urljoin

from pyimgflip import Config, MemeTemplate


def get_templates():
    r = requests.get(urljoin(Config.imgflip_api_url, 'get_memes'))
    if not r.json().get('success'):
        return {}
    return [MemeTemplate.from_request_data(m)
            for m in r.json().get('data', {}).get('memes', [])]


def get_template_by_id(id_):
    result = [t for t in get_templates() if t.id == str(id_)]
    return None if not result else result[0]


def get_template_by_name(name):
    result = [t for t in get_templates() if t.name.lower() == name.lower()]
    return None if not result else result[0]


def get_template_by_regex(pattern):
    result = [t for t in get_templates() if re.search(pattern, t.name, re.I)]
    return None if not result else result[0]


def get_meme_template_info():

    template_info = [(t.id, t.name, t.url) for t in get_templates()]

    headers = ['Template ID', 'Name', 'URL']
    widths = [max([len(header)] + [len(t[i]) for t in template_info])
              for i, header in enumerate(headers)]

    result = [' | '.join([h.center(w) for h, w in zip(headers, widths)])]
    result.extend(['-+-'.join(['-' * w for w in widths])])
    result.extend([' | '.join([t.ljust(w) for t, w in zip(item, widths)])
                   for item in template_info])

    return '\n'.join(result)
