"""
Models for databases
"""
from typing import List
import query
import yahoo
from aiogram.types import KeyboardButton
import datetime


class Portfolio:
    papers = []

    def __init__(self, port_id=None):
        if port_id is not None:
            self.load(port_id)
    
    def __str__(self):
        return f'{self.name} - {self.broker}'

    def update(self):
        """Update class to db"""
        query.update('portfolios', self.id, name=self.name, margin=self.margin, broker=self.broker)

    def save(self):
        """Save class to db if no entries or update"""
        query.insert('portfolios', name=self.name, broker=self.broker, margin=self.margin, holder_id=self.holder_id)

    def load(self, port_id):
        """Load class from db"""
        columns = ['id', 'name', 'holder_id', 'margin', 'broker']
        data = query.fetch('portfolios', columns=columns, id=port_id)
        if len(data) == 1:
            for col in columns:
                setattr(self, col, data[0][col])
            self.papers = [Paper(row['id']) for row in query.fetch('shares', ['id'], portfolio_id=self.id)]
        else:
            print('Found more then one entry')

    def command(self):
        return f'/port_{self.id}'

    def __is_in_db(self) -> bool:
        """Returns True if no entries in db"""
        try:
            return False if len(query.fetch('portfolios', [('id', self.id)])) == 0 else True
        except AttributeError:
            return False

    def value(self):
        """Value of portfolio"""
        value = 0
        for paper in self.papers:
            value += paper.value()
        return value

    def count_papers(self):
        return len(query.fetch('shares', ['id'], portfolio_id=self.id))

    def current_prices(self):
        """Get prices of all papers"""
        tickers = [f'{paper.ticker}.{paper.stock}' if paper.stock == 'ME' else paper.ticker for paper in self.papers]
        json = yahoo.get_json(tickers)
        self.current_value = 0
        for paper, price in zip(self.papers, json):
            paper.set_vars(price)
            self.current_value += paper.current_value()
        self.current_value = round(self.current_value, 2)

    def change(self):
        return round(self.current_value - self.value(), 2)

    def percent(self):
        return round(self.change() / self.value() * 100, 1)


class Paper:
    commission = 0

    def __init__(self, paper_id=None, **kwargs):
        if paper_id is not None:
            self.load(paper_id)
        else:
            try:
                self.ticker = kwargs['ticker'].upper()
                self.stock = kwargs['stock'].upper()
            except KeyError:
                pass

    def __str__(self):
        return f'{self.ticker}: {self.amount}. {self.command()}\n' \
               f'Price: {self.price} {self.currency}'

    def save(self):
        """Save class to db if no entries or update"""
        query.insert('shares', ticker=self.ticker, amount=self.amount, price=self.price, 
                     stock=self.stock, currency=self.currency, holder_id=self.holder_id, portfolio_id=self.portfolio_id,
                     commission=self.commission)
    
    def update(self):
        """Update class to db"""
        query.update('shares', self.id, 
                     ticker=self.ticker, amount=self.amount, stock=self.stock, currency=self.currency, price=self.price,
                     commission=self.commission)

    def load(self, paper_id):
        """Load class from db"""
        columns = ['id', 'ticker', 'amount', 'price', 'stock', 'currency', 'holder_id', 'portfolio_id', 'commission']
        data = query.fetch('shares', columns=columns, id=paper_id)
        if len(data) == 1:
            for col in columns:
                setattr(self, col, data[0][col])
            self.margin = query.fetch('portfolios', ['margin'], id=self.portfolio_id)[0]['margin']
        else:
            print('Found more then one entry')

    def delete(self):
        """Deletes from db"""
        query.delete('shares', id=self.id)

    def value(self):
        """Return value of paper"""
        return self.amount * self.price

    def current_value(self):
        return self.amount * self.current_price

    def get_yahoo(self):
        """ Gets JSON from YAHOO API"""
        price = yahoo.get_json([self.yahoo_ticker()])
        self.data = price[0]
        self.set_vars(self.data)

    def set_vars(self, data):
        """Maps variables from data JSON to separated important variables"""
        self.current_price = float(data['regularMarketPrice'])
        self.currency = data['currency']
        self.day_change = data['regularMarketChange']
        self.day_change_per = data['regularMarketChangePercent']
        self.name = data['shortName']
        self.market_state = data['marketState']

    def change(self):
        return round(self.current_value() - self.value(), 1)

    def percent(self):
        return round(self.change() / self.value() * 100, 1)

    def yahoo_ticker(self):
        return self.ticker if self.stock == 'NSDQ' else f'{self.ticker}.{self.stock}'

    def market(self):
        return f'Market price: {self.current_price} {self.currency} ' \
               f'{round(self.day_change, 2)} ({round(self.day_change_per, 2)})'

    def command(self):
        return f'/{self.ticker}_{self.portfolio_id}'

    def add_shares(self, amount, price):
        new_value = self.value() + amount * price
        self.amount += amount
        self.price = new_value / self.amount
        self.add_transaction(amount, price, self.update_commission(amount, price))
        self.update()

    def sell_shares(self, amount, price):
        self.amount -= amount
        self.add_transaction(-amount, price, self.update_commission(amount, price))
        self.update()

    def sell_all(self, price):
        self.add_transaction(-self.amount, price, self.update_commission(self.amount, price))
        # Add transaction
        pass

    def set_commission(self):
        """Sets commission paid to broker"""
        self.commission = self.value() * self.margin * 0.01

    def update_commission(self, amount, price):
        """ Adds new commission to already paid commission of this paper AND return commission of operation """
        self.commission += amount * price * self.margin * 0.01
        return amount * price * self.margin * 0.01

    def add_transaction(self, amount, price, commission):
        query.insert('transactions', ticker=self.ticker, amount=amount, price=price,
                     commission=commission, holder_id=self.holder_id, portfolio_id=self.portfolio_id,
                     share_id=self.id, date=datetime.datetime.utcnow())


class Stock:
    stock = ''
    kb = KeyboardButton(stock)

    def __init__(self, stock, symbol):
        self.stock = stock
        self.symbol = symbol
        self.kb = KeyboardButton(stock)


class Currency:
    currency = ''
    kb = KeyboardButton(currency)

    def __init__(self, stock, currency):
        self.stock = stock
        self.currency = currency
        self.kb = KeyboardButton(stock)