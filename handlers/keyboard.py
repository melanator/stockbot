from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from models import Stock, Currency

stocks_dict = {'Moscow Exchange': 'ME',
               'NASDAQ': 'NSDQ'}
curr_dict = {'Рубль': 'RUB',
             'Доллар': 'USD',
             'Евро': 'EUR'}

stocks = [Stock(name, sym) for name, sym in stocks_dict.items()]
currencies = [Currency(curr, sym) for curr, sym in curr_dict.items()]

stock_kb = ReplyKeyboardMarkup([[stock.kb for stock in stocks]], resize_keyboard=True)
currency_kb = ReplyKeyboardMarkup([[curr.kb for curr in currencies]], resize_keyboard=True)

cancel_kb = KeyboardButton('Cancel')
