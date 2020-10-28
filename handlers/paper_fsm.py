from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types
from misc import dp, bot
import stock
import messages
from models import Paper


# Bunch of handlers to create new paper.
class PaperFSM(StatesGroup):
    portfolio = State()
    ticker = State()
    amount = State()
    price = State()
    currency = State()

#New instance of Paper() class to save data
new_paper = Paper()


@dp.message_handler(lambda message: not message.text.startswith('/'), state=PaperFSM.portfolio)
async def wrong_input(message: types.Message):
    return await message.reply("Messages start with / don't work")


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=[r'^-?\d+(?:\.\d+)?$']), state=[PaperFSM.amount, PaperFSM.price])
async def not_number(message: types.Message):
    return await message.reply("Please, enter a number")


@dp.message_handler(commands=['newpaper'])
async def newpaper(message: types.Message):
    await PaperFSM.portfolio.set()
    answer_message = 'Choose your portfolio or create new:\nAvoid messages with /\n'
    answer_message += messages.message_portfolios(message.from_user, stock.fetch_portfolios(message.from_user))
    await message.reply(answer_message)


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """Allow user to cancel any action"""
    current_state = await state.get_state()
    if current_state is None:
        return
    # Cancel state and inform user about it
    await state.finish()
    await message.reply('Paper creating has been cancelled.')


@dp.message_handler(state=PaperFSM.portfolio)
async def paper_setportfolio_getticker(message: types.Message, state: FSMContext):
    new_paper.portfolio_id = stock.get_portfolio_id(message.text, message.user)
    new_paper.holder_id = message.user.id
    await PaperFSM.next()
    await message.reply("Portfolio selected.\nEnter ticker of paper")


@dp.message_handler(state=PaperFSM.ticker)
async def paper_setticker_getamount(message: types.Message, state: FSMContext):
    new_paper.ticker = message.text
    await PaperFSM.next()
    await message.reply("Enter amount of papers")


@dp.message_handler(state=PaperFSM.amount)
async def paper_setamount_getprice(message: types.Message, state: FSMContext):
    new_paper.amount = message.text
    await PaperFSM.next()
    await message.reply("Enter price of papers")


@dp.message_handler(state=PaperFSM.price)
async def paper_setprice_getcurrency(message: types.Message, state: FSMContext):
    new_paper.price = message.text
    await PaperFSM.next()
    await message.reply("Enter currency")


@dp.message_handler(state=PaperFSM.currency)
async def portfolio_setcurrency_finishmachine(message: types.Message, state: FSMContext):
    new_paper.currency = message.text
    new_paper.save()
    await bot.send_message(message.chat.id, 'Paper has been added to your portfolio')
    # Finish conversation
    await state.finish()
