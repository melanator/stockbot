"""
Models for databases
"""
from typing import List
import query


class Portfolio:
    def __init__(self, id=None):
        if id is not None:
            self.load(id)
    
    def __str__(self):
        return f'{self.name} - {self.broker}'

    def update(self):
        """Update class to db"""
        query.update('portfolios', self.id, name=self.name, margin=self.margin, broker=self.broker)

    def save(self):
        """Save class to db if no entries or update"""
        query.insert('portfolios', name=self.name, broker=self.broker, margin=self.margin, holder_id=self.holder_id)

    def load(self, id):
        """Load class from db"""
        data = query.fetch('portfolios', id=id)
        self.id, self.name, self.holder_id, self.margin, self.broker = data
      
    def command(self):
        return f'/{self.name}_{self.id}'

    def __is_in_db(self) -> bool:
        """Returns True if no entries in db"""
        try:
            return False if len(query.fetch('portfolios', [('id', self.id)])) == 0 else True
        except AttributeError:
            return False


class Paper:
    stock = '_blank'


    def __init__(self, id=None):
        if id is not None:
            self.load(id)

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

    def load(self, id):
        """Load class from db"""
        data = query.fetch('shares', id=id)
        self.id, self.ticker, self.amount, self.price, self.stock, self.currency, self.holder_id, self.portfolio_id = data
