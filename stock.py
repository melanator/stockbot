import query
import sqlite3
import messages


def start_bot(user: int):
    """Creates new entry in holders table."""
    try:
        query.insert('holders', {'id': user.id, 'name': user.username})
    except sqlite3.IntegrityError:
        pass
    return messages.message_start(user)


def portfolios(user: int):
    portfolios = fetch_portfolios(user)
    return messages.message_portfolios(user, portfolios)


def fetch_portfolios(user: int):
    """Fetch portfolios by user.user_id"""
    return query.fetch('portfolios', [('holder_id', user.id)])



def create_portfolio(name: str, broker: str, margin: float, holder_id: int):
    query.insert('portfolios', {'name': name,
                                'broker': broker,
                                'margin': margin,
                                'holder_id': holder_id})

def create_paper():
    pass

