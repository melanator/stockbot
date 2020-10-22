from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from misc import dp, bot
import stock
import messages


# Bunch of handlers to create new paper.
class PaperFSM(StatesGroup):
    portfolio = State()
    ticker = State()
    amount = State()
    price = State()


@dp.message_handler(commands=['newpaper'])
async def new_paper(message: types.Message):
    await PaperFSM.portfolio.set()
    answer_message = 'Choose your portfolio or create new:\n'
    answer_message += messages.message_portfolios(message.from_user, stock.fetch_portfolios(message.from_user))
    await message.reply(answer_message)


@dp.message_handler(state=PaperFSM.portfolio)
async def paper_setportfolio_getticker(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['portfolio'] = message.text
    await PaperFSM.next()
    await message.reply("Enter ticker of paper")


@dp.message_handler(state=PaperFSM.ticker)
async def paper_setticker_getamount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ticker'] = message.text
    await PaperFSM.next()
    await message.reply("Enter amount of papers")


@dp.message_handler(state=PaperFSM.amount)
async def paper_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await PaperFSM.next()
    await message.reply("Enter amount of papers")


@dp.message_handler(state=PaperFSM.price)
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