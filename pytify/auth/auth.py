import os
import requests
import base64
import json

from .authorization import Authorization
from pytify.core import BadRequestError
from .auth_method import AuthMethod


def _authorization_code(conf):

    current_dir = os.path.abspath(os.curdir)
    file_path = os.path.join(current_dir, '.pytify')

    auth_key = get_auth_key(conf.client_id, conf.client_secret)

    try:
        with open(file_path, mode='r', encoding='UTF-8') as file:
            refresh_token = file.readline()

            if refresh_token:
                return _refresh_access_token(auth_key, refresh_token)
    except IOError:
        raise IOError(('It seems you have not authorize the application '
                       'yet. The file .pytify was not found.'))


def _refresh_access_token(auth_key, refresh_token):

    headers = {'Authorization': f'Basic {auth_key}', }

    options = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        }

    response = requests.post(
        'https://accounts.spotify.com/api/token',
        headers=headers,
        data=options
    )

    content = json.loads(response.content.decode('utf-8'))

    if not response.ok:
        error_description = content.get('error_description', None)
        raise BadRequestError(error_description)

    access_token = content.get('access_token', None)
    token_type = content.get('token_type', None)
    scope = content.get('scope', None)
    expires_in = content.get('expires_in', None)

    return Authorization(access_token, token_type, expires_in, scope, None)




# Function sends the request to the Spotify account service and return the access token
def get_auth_key(client_id, client_secret):
    # convert the string in client_id and client_secret to bytes
    byte_keys = bytes(f'{client_id: {client_secret}}', 'utf-8')
    # Encode the bytes using base 64
    encoded_key = base64.b64encode(byte_keys)
    # Decode it returning the string representation of encoded data
    return encoded_key.decode('utf-8')


def _client_credentials(conf):  # Takes an argument of the configuration
    """
    uses the get_auth_key function to pass the client_id
    and the client_secret to build a base 64-encoded auth_key
    """
    auth_key = get_auth_key(conf.client_id, conf.client_secret)

    # setting the Authorization in the request header
    headers = {'Authorization': f'Basic {auth_key}', }

    options = {
        'grant_type': 'client_credentials',
        'json': True,  # tells the API that we want the response in JSON format
    }

    """
    Use the requests package to make the request to spotify's account service
    passing the headers and data configured
    """
    response = requests.post(
        'https://accounts.spotify.com/api/token',
        headers=headers,
        data=options
    )

    content = json.loads(response.content.decode('utf-8'))
    # After getting a response the JSON data gets decoded and loaded into the variable content
    if response.status_code == 400:
        error_description = content.get('error_description', '')
        raise BadRequestError(error_description)

    access_token = content.get('access_token', None)
    token_type = content.get('token_type', None)
    expires_in = content.get('expires_in', None)
    scope = content.get('scope', None)

    return Authorization(access_token, token_type, expires_in,
                         scope, None)


def authenticate(conf): #returns all the data that has been read from the configuration file
    if conf.auth_method == AuthMethod.CLIENT_CREDENTIALS:
        return _client_credentials(conf)
    """
    Configuration gets passed to _client_credentials,
    which will obtain the access_token
    """
    return _client_credentials(conf)

