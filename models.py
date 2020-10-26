"""
Models for databases
"""
from typing import List
import query
import stock


class Portfolio:
    def __init__(self, query_result: List):
        self.id = query_result[0]
        self.name = query_result[1]
        self.holder_id = query_result[2],
        self.margin = query_result[3]
        self.broker = query_result[4]

    def __str__(self):
        return f'{self.name} - {self.broker}'

    def save(self):
        """Update class to db"""
        query.update('portfolios', self.id, 
                    [('name', self.name), ('margin', self.margin), ('broker', self.broker)])

    def command(self):
        return f'/{self.name}_{self.id}'


class Paper:
    def __init__(self, query_result: List):
        self.id = query_result[0],
        self.ticker = query_result[1],
        self.amount = query_result[2],
        self.price = query_result[3],
        self.stock = query_result[4],
        self.currency = query_result[5],
        self.holder_id = query_result[6],
        self.portfolio_id = query_result[7]

    def __str__(self):
        return f'{self.ticker} - {self.amount} pcs. Price: {self.price}{self.stock}'

    def save(self):
        """Update class to db"""
        query.update('shares', self.id, 
                    [('ticker', self.ticker), ('amount', self.amount), ('stock', self.stock), ('currency', self.currency)])
