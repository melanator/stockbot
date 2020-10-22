from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from ..misc import dp
import stock

storage = MemoryStorage()


# Bunch of handlers to create new paper.
class Paper(StatesGroup):
    portfolio = State()
    ticker = State()
    amount = State()
    price = State()


@dp.message_handler(commands=['newpaper'])
async def new_paper(message: types.Message):
    await Paper.portfolio.set()
    await message.reply("Choose your portfolio or create new")


@dp.message_handler(state=Paper.portfolio)
async def paper_setportfolio_getticker(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['portfolio'] = message.text
    await Paper.next()
    await message.reply("Enter ticker of paper")


@dp.message_handler(state=Paper.ticker)
async def paper_setticker_getamount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ticker'] = message.text
    await Paper.next()
    await message.reply("Enter amount of papers")


@dp.message_handler(state=Paper.amount)
async def paper_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await Paper.next()
    await message.reply("Enter amount of papers")


@dp.message_handler(state=Paper.price)
async def portfolio_setprice_finishstates(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

        # Add entry
        stock.create_portfolio(data['portfolio'],
                               data['ticker'],
                               data['amount'], 
                               data['price'],
                               message.from_user.id)
    await bot.send_message(message.chat.id,'Ticker has been added')
    # Finish conversation
    await state.finish()