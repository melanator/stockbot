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
        for p in portfolios:
            message += f'{p} {p.command()}\n'
            if p.count_papers() > 0:
                p.current_prices()
                message += f'{p.current_value} {p.change()} ({p.percent()}%)\n\n'
            else:
                message += f'No papers\n\n'
    else:
        message += 'You have no portfolios\n'
    message += 'Create new /newportfolio\n'
    return message


def portfolio(portfolio_id):
    """Message of /port_*id* command"""
    port = Portfolio(portfolio_id)
    if port.count_papers() > 0:
        message = 'Your papers\n'
        port.current_prices()
        for paper in port.papers:
            message += f'{paper}\n' \
                       f'{paper.change()} {paper.currency} ({paper.percent()}%) \n' \
                       f'{paper.market()}\n\n'
        return message
    else:
        return "No papers"


def paper(ticker, portfolio_id, user):
    """Message of /ticker_port_id command"""
    paper = stock.get_paper(ticker, portfolio_id, user.id)
    if paper:
        paper.get_yahoo()
        message = f'{paper}\n' \
                   f'{paper.change()} {paper.currency} ({paper.percent()}%) \n' \
                   f'{paper.market()}\n\n'
        return message
    else:
        return 'No such paper'


def sell_shares():
    pass


def add_shares():
    pass


def sell_all():
    pass
