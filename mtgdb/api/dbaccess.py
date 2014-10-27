"""
This is the main module for accessing the MTGDB.info database. In most cases,
all calls to find a card or set of cards should go through this module.
"""

from models import Card, CardSet
from config import MTG_DB_URL, CARDS_PATH, SETS_PATH, RANDOM_CARD_PATH
import requests

def get_card(name=None, id=None):
    """
    Retrieves a card from the database using a name or card id. If both name
    and id are provided, only the id will be used. If neither id nor name are
    provided this function will return a random card.

    :param name: Optional. Specifies the name of the card to retrieve.
    :param id: Optional. Specifies the id of the card to retrieve.
    :returns: A Card object.
    """
    card_url = "{0}{1}{2}"
    if id:
        r = requests.get(card_url.format(MTG_DB_URL,
                                         CARDS_PATH,
                                         id))
        if(r.status_code != 200):
            raise Exception("No card found by that id.")
        else:
            return Card(r.json())
    elif name:
        r = requests.get(card_url.format(MTG_DB_URL,
                                         CARDS_PATH,
                                         clean_card_name(name)))
        if(r.status_code != 200):
            raise Exception("No card found by that name.")
        else:
            return Card(r.json())
    else:
        return get_random_card()

def get_random_card(set=None):
    """
    Retrieves a random card from the MTGDB.info database and returns it.

    :param set: Optional. Specifies a set from which to retrieve a random card.
    :returns: A Card object.
    """
    if(set):
        req_url = '{0}{1}{2}{3}'.format(MTG_DB_URL,
                                        SETS_PATH,
                                        set,
                                        RANDOM_CARD_PATH)
        r = requests.get(req_url)
        if(r.status_code != 200):
            raise Exception('There was a problem finding a random card.\
                             Please ensure card set {0} exists'.format(set))
        else:
            return Card(r.json())
    else:
        req_url = '{0}{1}'.format(MTG_DB_URL, RANDOM_CARD_PATH)
        r = requests.get(req_url)
        if(r.status_code != 200):
            raise Exception('There was a problem finding a random card.')
        else:
            return Card(r.json())

def clean_card_name(s):
    """
    Removes characters from a card name that can't be used in a request to
    the MTGDB.info database.

    :param s: The string to be cleaned.
    :returns: A safe string that can be used in a request.
    """
    return s.replace(':', '')