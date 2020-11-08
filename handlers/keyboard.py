from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from models import Stock, Currency

stocks_dict = {'Moscow Exchange': 'ME',
               'NASDAQ': 'NSDQ'}
curr_dict = {'Рубль': 'RUB',
             'Доллар': 'USD',
             'Евро': 'EUR'}

stocks = [Stock(name, sym) for name, sym in stocks_dict.items()]
currencies = [Currency(curr, sym) for curr, sym in curr_dict.items()]
cancel_button = KeyboardButton('Cancel')

stock_kb = ReplyKeyboardMarkup([[stock.kb for stock in stocks], [cancel_button]], resize_keyboard=True)
currency_kb = ReplyKeyboardMarkup([[curr.kb for curr in currencies]], resize_keyboard=True)
paper_kb = ReplyKeyboardMarkup([['Add shares', 'Sell shares'], ['Sell all', 'Delete position']],
                               resize_keyboard=True)
cancel_kb = ReplyKeyboardMarkup([[cancel_button]], resize_keyboard=True)

