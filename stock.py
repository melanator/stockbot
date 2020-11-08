import query
import sqlite3
import messages
from typing import List
from models import Portfolio, Paper


def start_bot(user):
    """Creates new entry in holders table."""
    try:
        query.insert('holders', id=user.id, name=user.username)
    except sqlite3.IntegrityError:
        pass


def fetch_portfolios(user):
    """Fetch portfolios by user.user_id"""
    data = query.fetch('portfolios', ['id'], holder_id=user.id)
    return [Portfolio(x['id']) for x in data]


def get_portfolio_id(name, user):
    """Finds id of portfolio by its name and holder_id"""
    return query.fetch('portfolios', ['id'], name=name, holder_id=user.id)


def is_user_holds_portfolio(user_id: int, portfolio_id: int) -> bool:
    """Checks if user_id has portfolio_id"""
    return True if len(query.fetch('portfolios', ['id'], holder_id=user_id, id=portfolio_id)) > 0 else False


def get_portfolio_papers(portfolio_id: int):
    return [Paper(row['id']) for row in query.fetch('shares', ['id'], portfolio_id=portfolio_id)]


def get_paper(ticker: str, portfolio_id: int, holder_id: int) -> Paper:
    try:
        return Paper(query.fetch('shares', ['id'], ticker=ticker, holder_id=holder_id, portfolio_id=portfolio_id)[0]['id'])
    except IndexError:
        return
