from collections import namedtuple

"""Authentication model that will contain the data we get after requesting an access token"""
Authorization = namedtuple('Authorization', [
    'access_token',  # The token that's sent with every request to the web api
    'token_type',  # The type of token, which is usually Bearer
    'expires_in',  # access_token expiration time (1 hour)
    'scope',  # Permission that spotify's user granted to our application
    'refresh_token',  # The token that can be used to refresh the access_token after expiration
])
