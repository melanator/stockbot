"""
Models for databases
"""
from typing import List


class Portfolio:
    def __init__(self, query_result: List):
        self.id = query_result[0]
        self.name = query_result[1]
        self.holder_id = query_result[2],
        self.margin = query_result[3]
        self.broker = query_result[4]

    def __str__(self):
        return f'{self.name} - {self.broker}'


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