from typing import List
from models import Portfolio
import stock


def start(user):
    """Message of /start command"""
    stock.start_bot(user)
    message = f"Hi, {user.first_name}!\n"
    message += 'To see your portfolios /portfolios\n'
    return message


def portfolios(user):
    """Message of /portfolios command"""
    portfolios = stock.fetch_portfolios(user)
    message = ''
    if len(portfolios) > 0:
        message += 'Your portfolios:\n'
        for row in portfolios:
            message += f'{row} {row.command()}\n'
    else:
        message += 'You have no portfolios\n'
    message += 'Create new /newportfolio\n'
    return message


def portfolio(portfolio_id):
    """Message of /port_*id* command"""
    message = 'Your papers\n'
    papers = stock.get_portfolio_papers(portfolio_id)
    for paper in papers:
        message += f'{paper}\n'

    return message




