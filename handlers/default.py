import messages
from misc import dp
from aiogram import types
from aiogram.dispatcher import filters
import re
import stock
import handlers.keyboard as kb


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    await message.reply(messages.start(message.from_user), reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['portfolios'])
async def show_portfolios(message: types.Message):
    await message.reply(messages.portfolios(message.from_user))


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['port_\d+']))
async def portfolio(message: types.Message):
    port_id = re.search(r'\d+', message.text).group(0)
    if stock.is_user_holds_portfolio(message.from_user.id, port_id):
        await message.reply(messages.portfolio(port_id))



