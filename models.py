"""
Models for databases
"""
from typing import List
import query
import yahoo


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

    def commission(self):
        """Return commission paid to broker"""
        return self.value() * self.portfolio.margin

    def current_prices(self):
        """Get prices of all papers"""
        tickers = [f'{paper.ticker}.{paper.stock}' if paper.stock == 'ME' else paper.ticker for paper in self.papers]
        json = yahoo.get_json(tickers)
        for paper, price in zip(self.papers, json):
            paper.current_price = float(price['regularMarketPrice'])

    def sum_papers_change(self):
        pass

    def portfolio_change(self):
        pass


class Paper:
    def __init__(self, paper_id=None):
        if paper_id is not None:
            self.load(paper_id)

    def __str__(self):
        return f'{self.ticker} - {self.amount} pcs. Price: {self.price} {self.currency}'

    def save(self):
        """Save class to db if no entries or update"""
        query.insert('shares', ticker=self.ticker, amount=self.amount, price=self.price, 
                     stock=self.stock, currency=self.currency, holder_id=self.holder_id, portfolio_id=self.portfolio_id)
    
    def update(self):
        """Update class to db"""
        query.update('shares', self.id, 
                     ticker=self.ticker, amount=self.amount, stock=self.stock, currency=self.currency)

    def load(self, paper_id):
        """Load class from db"""
        columns = ['id', 'ticker', 'amount', 'price', 'stock', 'currency', 'holder_id', 'portfolio_id']
        data = query.fetch('shares', columns=columns, id=paper_id)
        if len(data) == 1:
            for col in columns:
                setattr(self, col, data[0][col])
            self.margin = query.fetch('portfolios', ['margin'], id=self.portfolio_id)[0]['margin']
        else:
            print('Found more then one entry')

    def value(self):
        """Return value of paper"""
        return self.amount * self.price

    def commission(self):
        """Return commission paid to broker"""
        return self.value() * self.portfolio.margin

    def get_current_price(self):
        price = yahoo.get_json([f'{self.ticker}.{self.stock}' if self.stock == 'ME' else self.ticker])
        self.current_price = float(price["regularMarketPrice"])

    def change(self):
        return round(self.current_price * self.amount - self.value(), 2)

    def percent(self):
        return round((self.current_price * self.amount - self.value()) * 100 / self.value(), 2)
