import os


class Config(object):

    imgflip_api_url = (os.environ.get('IMGFLIP_API_URL')
                       or 'https://api.imgflip.com')

    imgflip_username = (os.environ.get('IMGFLIP_USERNAME')
                        or 'theceebee')

    imgflip_password = (os.environ.get('IMGFLIP_PASSWORD')
                        or 'password123')
