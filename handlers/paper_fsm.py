from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from misc import dp, bot
import stock
import messages
from models import Paper
import re

# Bunch of handlers to create new paper.
class PaperFSM(StatesGroup):
    portfolio = State()
    ticker = State()
    amount = State()
    price = State()
    currency = State()


# New instance of Paper() class to save data
new_paper = Paper()


@dp.message_handler(lambda message: not message.text.startswith('/port_'), state=PaperFSM.portfolio)
async def wrong_input(message: types.Message):
    return await message.reply("Choose portfolio by clicking on /port_ command")


@dp.message_handler(commands=['newpaper'])
async def newpaper(message: types.Message):
    await PaperFSM.portfolio.set()
    answer_message = 'Choose your portfolio or create new:\nAvoid messages with /\n'
    answer_message += messages.portfolios(message.from_user)
    await bot.send_message(message.chat.id, answer_message)


# You can use state '*' if you need to handle all states
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(filters.Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """Allow user to cancel any action"""
    current_state = await state.get_state()
    if current_state is None:
        return
    # Cancel state and inform user about it
    await state.finish()
    await bot.send_message(message.chat.id, 'Paper creating has been cancelled.')


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['port_\d+$']), state=PaperFSM.portfolio)
async def paper_setportfolio_getticker(message: types.Message, state: FSMContext):
    new_paper.portfolio_id = re.search(r'\d+', message.text).group(0)
    new_paper.holder_id = message.from_user.id
    if stock.is_user_holds_portfolio(new_paper.holder_id, new_paper.portfolio_id):
        await PaperFSM.next()
        await bot.send_message(message.chat.id, "Portfolio selected.\nEnter ticker of paper")
    else:
        await message.reply("Choose YOUR portfolio")


@dp.message_handler(state=PaperFSM.ticker)
async def paper_setticker_getamount(message: types.Message, state: FSMContext):
    new_paper.ticker = message.text.upper()
    await PaperFSM.next()
    await bot.send_message(message.chat.id, "Enter amount of papers")


@dp.message_handler(filters.Regexp(regexp='^-?\d+(?:\.\d+)?$'), state=PaperFSM.amount)
async def paper_setamount_getprice(message: types.Message, state: FSMContext):
    new_paper.amount = message.text
    await PaperFSM.next()
    await bot.send_message(message.chat.id, "Enter price of papers")


@dp.message_handler(filters.Regexp(regexp='^-?\d+(?:\.\d+)?$'), state=PaperFSM.price)
async def paper_setprice_getcurrency(message: types.Message, state: FSMContext):
    new_paper.price = message.text
    await PaperFSM.next()
    await bot.send_message(message.chat.id, "Enter currency")


@dp.message_handler(state=PaperFSM.currency)
async def portfolio_setcurrency_finishmachine(message: types.Message, state: FSMContext):
    new_paper.currency = message.text
    new_paper.save()
    await bot.send_message(message.chat.id, f'Paper has been added to your portfolio\n{new_paper}')
    # Finish conversation
    await state.finish()
