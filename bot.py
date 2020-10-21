"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import config
import stock

API_TOKEN = config.BOT_TOKEN

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Portfolio(StatesGroup):
    portfolio = State()
    broker = State()
    margin = State()


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
    """
    Creates new entry in holders tables if user is new.
    """
    stock.start_bot(message.from_user.id, message.from_user.username)
    rows = stock.get_portfolios(message.from_user.id)
    message_text = f"Hi, {message.from_user.first_name}!\n"
    if len(rows) > 0:
        message_text += 'Your portfolios:\n'
        for row in rows:
            message_text += f'{row}\n'
    else:
        message_text += 'You have no portfolios\n'
    message_text += 'Create new /newportfolio\n'
    await message.reply(message_text)

"""
Bunch of handlers to create new portfolio
"""


@dp.message_handler(commands=['newportfolio'])
async def new_portfolio(message: types.Message):
    await Portfolio.portfolio.set()
    await message.reply("Enter name of portfolio")


@dp.message_handler(state=Portfolio.portfolio)
async def process_portfolio(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['portfolio'] = message.text

    await Portfolio.next()
    await message.reply("Enter name of your broker")


@dp.message_handler(state=Portfolio.broker)
async def process_broker(message: types.Message, state: FSMContext):
    """
    Process user name
    """
    async with state.proxy() as data:
        data['broker'] = message.text

    await Portfolio.next()
    await message.reply("Enter your margin")


@dp.message_handler(state=Portfolio.margin)
async def process_margin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['margin'] = message.text

        # Add entry
        stock.create_portfolio(data['portfolio'],
                               data['broker'],
                               data['margin'],
                               message.from_user.id)
    # Send message
    await bot.send_message(message.chat.id,'Portfolio has been added')

    # Finish conversation
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    bot.infinity_polling()
