from enum import Enum, auto

class AuthMethod(Enum):
    """
    Enumeration to represent both
    kinds of authentication from spotify
    """
    CLIENT_CREDENTIALS = auto()
    AUTHORIZATION_CODE = auto()
