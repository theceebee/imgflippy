import sys
import logging
import argparse
import textwrap

import pyimgflip
from pyimgflip import Config, MemeTemplate
from pyimgflip import model
from pyimgflip import utils


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(pyimgflip.__name__)


class TemplateAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if option_string in ['-i', '-id']:
            template = utils.get_template_by_id(values)
        elif option_string in ['-n', '--name']:
            template = utils.get_template_by_name(values)
        elif option_string in ['-r', '--regex']:
            template = utils.get_template_by_regex(values)
        setattr(namespace, self.dest, template or values)


class BoxesAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        boxes_ = getattr(namespace, 'boxes', [])

        consumed = False

        for box in boxes_:
            if self.dest in box:
                continue

            box.update({self.dest: values})
            consumed = True
            break

        if not consumed:
            boxes_.append({self.dest: values})

        setattr(namespace, 'boxes', boxes_)


def main():

    parser_ = argparse.ArgumentParser(
        prog=pyimgflip.__name__,
        description=textwrap.dedent('''\
            An unofficial and open source Python interface for the imgflip 
            RESTful API (https://api.imgflip.com/).'''),
        formatter_class=argparse.RawTextHelpFormatter)

    parser_.add_argument(
        '-v',
        '--version',
        action='store_true',
        default=argparse.SUPPRESS,
        help='display the program\'s version and exit.')

    subparsers = parser_.add_subparsers(dest='cmd', metavar='COMMAND')
    subparsers.add_parser(
        name='get_memes',
        help='Display a list of available meme templates and exit.')

    add_caption_parser = subparsers.add_parser(
        name='add_caption',
        formatter_class=argparse.RawTextHelpFormatter,
        help='Add a caption to meme template and print the resulting meme\'s '
             'image URL.')

    template_group = add_caption_parser.add_mutually_exclusive_group(
        required=True)

    template_group.add_argument(
        '-i',
        '--id',
        action=TemplateAction,
        help='Find meme template by id.',
        metavar='ID',
        dest='template')

    template_group.add_argument(
        '-n',
        '--name',
        action=TemplateAction,
        help='Find meme template by name.',
        metavar='NAME',
        dest='template')

    template_group.add_argument(
        '-r',
        '--regex',
        action=TemplateAction,
        help='Find meme template by regular expression.',
        metavar='REGEX',
        dest='template')

    add_caption_parser.add_argument(
        '-u',
        '--username',
        default=Config.imgflip_username,
        help='Username of a valid imgflip account.\nThis is used to track '
             'where API requests are coming from.')

    add_caption_parser.add_argument(
        '-p',
        '--password',
        default=Config.imgflip_password,
        help='Password for the imgflip account.')

    add_caption_parser.add_argument(
        '-t0',
        '--text0',
        default=argparse.SUPPRESS,
        help='Top text for the meme (do not use this argument if you are '
             'using the boxes "text" argument below).',
        metavar='TEXT',
        dest='text0')

    add_caption_parser.add_argument(
        '-t1',
        '--text1',
        default=argparse.SUPPRESS,
        help='bottom text for the meme (do not use this argument if you are \n'
             'using the boxes \'text\' argument below).',
        metavar='TEXT',
        dest='text1')

    add_caption_parser.add_argument(
        '-f',
        '--font',
        default=argparse.SUPPRESS,
        choices=model.Fonts.valid(),
        help='The font family to use for the text.\nCurrent options are '
             '"impact" and "arial" (defaults to impact)',
        metavar='FONT')

    add_caption_parser.add_argument(
        '-m',
        '--max-font-size',
        default=argparse.SUPPRESS,
        type=int,
        help='Maximum font size in pixels (defaults to 50px).',
        metavar='SIZE')

    boxes_group = add_caption_parser.add_argument_group(
        title='boxes',
        description=textwrap.dedent('''\
            For creating memes with more than two text boxes, or for further 
            customization.
            
            If boxes arguments are specified, text0 and text1 will be ignored,
            and text will not be automatically converted to uppercase, so
            you'll have to handle capitalization yourself if you want the
            standard uppercase meme text. You may specify up to 5 text boxes.
            All options below are optional, except "text". The exception is
            that you may leave the first box completely empty, so that the
            second box will automatically be used for the bottom text.
            
            Arguments x, y, width and height are for the bounding box of the
            text box. Arguments x and y are the coordinates of the top left
            corner. If you specify bounding coordinates, be sure to specify all
            four (x, y, width, height), otherwise your text may not show up
            correctly. If you do not specify bounding box coordinates, the same
            automatic default coordinates from imgflip.com/memegenerator will
            be used, which is very useful for memes with special text box
            positioning other than the simple top/bottom.'''))

    boxes_group.add_argument('-t',
                             '--text',
                             action=BoxesAction,
                             default=argparse.SUPPRESS,
                             dest='text')

    boxes_group.add_argument('-x',
                             action=BoxesAction,
                             default=argparse.SUPPRESS,
                             type=int,
                             dest='x')

    boxes_group.add_argument('-y',
                             action=BoxesAction,
                             default=argparse.SUPPRESS,
                             type=int,
                             dest='y')

    boxes_group.add_argument('-w',
                             '--width',
                             action=BoxesAction,
                             default=argparse.SUPPRESS,
                             type=int,
                             dest='width')

    boxes_group.add_argument('-H',
                             '--height',
                             action=BoxesAction,
                             default=argparse.SUPPRESS,
                             type=int,
                             dest='height')

    boxes_group.add_argument('-c',
                             '--color',
                             action=BoxesAction,
                             default=argparse.SUPPRESS,
                             dest='color')

    boxes_group.add_argument('-o',
                             '--outline-colour',
                             action=BoxesAction,
                             default=argparse.SUPPRESS,
                             dest='outline_color')

    args = parser_.parse_args()

    if hasattr(args, 'version'):
        message = '{} v{}'.format(pyimgflip.__name__, pyimgflip.__version__)
        parser_.exit(status=0, message=message)

    if not args.cmd:
        parser_.error(message='too few arguments')

    # Display a table of the templates available for captioning.
    if args.cmd == 'get_memes':
        return parser_.exit(status=0, message=utils.get_meme_template_info())

    elif args.cmd == 'add_caption':
        if not isinstance(args.template, MemeTemplate):
            raise RuntimeError

        kwargs = {k: v for k, v in vars(args).items() if
                  k not in ['cmd', 'template']}

        result = args.template.add_caption(**kwargs)
        print(result.url)

    sys.exit(0)


main()
