from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from ..misc import dp
import stock


storage = MemoryStorage()
# Bunch of handlers to create new portfolio. Needs to move out. 
class Portfolio(StatesGroup):
    portfolio = State()
    broker = State()
    margin = State()


@dp.message_handler(commands=['newportfolio'])
async def new_portfolio(message: types.Message):
    await Portfolio.portfolio.set()
    await message.reply("Enter name of portfolio")


@dp.message_handler(state=Portfolio.portfolio)
async def portfolio_setportfolio_getbroker(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['portfolio'] = message.text
    await Portfolio.next()
    await message.reply("Enter name of your broker")


@dp.message_handler(state=Portfolio.broker)
async def portfolio_setbroker_getmargin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['broker'] = message.text
    await Portfolio.next()
    await message.reply("Enter your margin")


@dp.message_handler(state=Portfolio.margin)
async def portfolio_setmargin_finishstates(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['margin'] = message.text

        # Add entry
        stock.create_portfolio(data['portfolio'],
                               data['broker'],
                               data['margin'],
                               message.from_user.id)
    await bot.send_message(message.chat.id,'Portfolio has been added')
    # Finish conversation
    await state.finish()
