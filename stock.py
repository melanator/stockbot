import query
import sqlite3
import messages
from typing import List
from models import Portfolio


def start_bot(user):
    """Creates new entry in holders table."""
    try:
        query.insert('holders', {'id': user.id, 'name': user.username})
    except sqlite3.IntegrityError:
        pass
    return messages.message_start(user)


def portfolios(user) -> List[Portfolio]:
    """
    Makes query to db and return list of portfolio classes
    """
    rows = fetch_portfolios(user)
    portfolios_classes = []
    for row in rows:
        portfolios_classes.append(Portfolio(row))
    return messages.message_portfolios(user, portfolios_classes)


def fetch_portfolios(user):
    """Fetch portfolios by user.user_id"""
    return query.fetch('portfolios', [('holder_id', user.id)])


def create_portfolio(name: str, broker: str, margin: float, holder_id: int):
    query.insert('portfolios', {'name': name,
                                'broker': broker,
                                'margin': margin,
                                'holder_id': holder_id})


def create_paper():
    pass

