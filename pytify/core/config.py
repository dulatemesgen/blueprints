import os
import yaml
from collections import namedtuple

from pytify.auth import auth_method


# a model representing the configuration file
Config = namedtuple('Config', ['client_id',
                               'client_secret',
                               'access_token_url',
                               'auth_url',
                               'api_version',
                               'api_url',
                               'base_url',
                               'auth_method', ])


def read_config():
    """Loads YAML file and returns the namedtuple config"""

    current_dir = os.path.abspath(os.curdir) # Gets the absolute path of the current directory and assigns it to the variable current_dir
    file_path = os.path.join(current_dir, 'config.yaml') # Join the path stored on the current_dir variable with the YAML configuration file

    try:
        with open(file_path, mode='r', encoding='UTF-8') as file: # open file as read-only and set UTF-8 encoding

             """call the load function in the
            yaml module to load and parse the
            file, and assign the results to the config variable"""
            config = yaml.load(file)

            # base_url is a helper value that contains the concatenated values of api_url and api_version
            config['base_url'] = f'{config["api_url"]}/{config["api_version"]}'

            auth_method = config['auth_method']
            config['auth_method'] =
            AuthMethod.__members__.get(auth_method)

            return Config(**config)

        except IOError as e:
            """If file can't be read or opened, this will print a help message to the user
            saying that it couldn't open the file and will show how the YAML configuration should be"""

            print(""" Error: couldn't find the configuration file 
            'config.yaml'
            'on your current directory.

            Default format is:',

            client_id: 'your_client_id'
                     client_secret: 'you_client_secret'
            access_token_url: 'https://accounts.spotify.com/api/token'
            auth_url: 'http://accounts.spotify.com/authorize'
            api_version: 'v1'
            api_url: 'http//api.spotify.com'
                uth_method: 'authentication method'

            * auth_method can be CLIENT_CREDENTIALS or
            AUTHORIZATION_CODE""")
            raise
