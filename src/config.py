from json import load
from os.path import isfile


def get_config():
    token: str = None

    # Config vars
    if not isfile('config.json'):
        raise FileNotFoundError()
    with open('config.json') as f:
        conf = load(f)
    token = conf.get('api_token')
    admins = conf.get('admins_uid')

    return token, admins


WELLCOME_MESSAGE = '''
    Hello,
    
    I was created to serve as client for a MRI implementation made by Roberto Martí and Leonel Alejandro. 
    
    You can start by choosing a dataset. :)
'''

HELP_MESSAGE = '''
Your choices are limited here, you have to choose between the commands below or simply send me a query.

/help - Show this message.

/choose_dataset - Obvious.

/get_report - Upload the report of this project with the source code.

'''
