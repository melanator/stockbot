import query
import sqlite3
import messages
from typing import List
from models import Portfolio

def start_bot(user):
    """Creates new entry in holders table."""
    try:
        query.insert('holders', id=user.id, name=user.username)
    except sqlite3.IntegrityError:
        pass
    return messages.message_start(user)


def fetch_portfolios(user):
    """Fetch portfolios by user.user_id"""
    portfolios_ids = query.fetch('portfolios', ['id'], holder_id=user.id)
    return [Portfolio(id) for id in portfolios_ids]


def get_portfolio_id(name, user):
    """Finds id of portfolio by its name and holder_id"""
    return query.fetch('portfolios', ['id'], name='name', holder_id=user.id)
