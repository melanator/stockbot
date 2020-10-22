import stock
from misc import dp
from aiogram import types


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.reply(stock.start_bot(message.from_user))


@dp.message_handler(commands=['portfolios'])
async def show_portfolios(message: types.Message):
    await message.reply(stock.portfolios(message.from_user))