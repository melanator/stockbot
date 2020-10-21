import query
import sqlite3


def start_bot(user_id: int, username: str):
    """
    Creates new entry in holders table.
    """
    try:
        query.insert('holders', {'id': user_id, 'name': username})
    except sqlite3.IntegrityError:
        pass


def get_portfolios(holder_id: int):
    return query.fetch('portfolios', [('holder_id', holder_id)])


def create_portfolio(name: str, broker: str, margin: float, holder_id: int):
    query.insert('portfolios', {'name': name,
                                'broker': broker,
                                'margin': margin,
                                'holder_id': holder_id})
