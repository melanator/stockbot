from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from misc import dp, bot
import stock
import messages
import yahoo
from models import Paper
import re

# Bunch of handlers to create new paper.
class PaperFSM(StatesGroup):
    portfolio = State()
    stock = State()
    ticker = State()
    amount = State()
    price = State()
    currency = State()


""" New instance of Paper() class to save data """
new_paper = Paper()

""" Start of FSM """
@dp.message_handler(commands=['newpaper'])
async def newpaper(message: types.Message):
    await PaperFSM.portfolio.set()
    answer_message = 'Choose your portfolio or create new:\nAvoid messages with /\n'
    answer_message += messages.portfolios(message.from_user)
    await bot.send_message(message.chat.id, answer_message)


""" When choosing portfolio message doesn't start with /port """
@dp.message_handler(lambda message: not message.text.startswith('/port_'), state=PaperFSM.portfolio)
async def wrong_input(message: types.Message):
    return await message.reply("Choose portfolio by clicking on /port_ command")

""" Cancel FSM with cancel command """
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


"""
Selecting portfolio by message /port_id, id in database 'portfolios' table. Checking is portfolio owned by user.
Then choosing stock by keyboard
""" 
@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['port_\d+$']), state=PaperFSM.stock)
async def paper_setportfolio_getstock(message: types.Message, state: FSMContext):
    new_paper.portfolio_id = re.search(r'\d+', message.text).group(0)
    new_paper.holder_id = message.from_user.id
    new_paper.stock = message.text.upper()
    await PaperFSM.next()
    if stock.is_user_holds_portfolio(new_paper.holder_id, new_paper.portfolio_id):
        await bot.send_message(message.chat.id, "Portfolio selected.\nChoose stock: NASDAS, MOEX, DAX")
        # Добавить кнопки выбора биржи
    else:
        await message.reply("Choose YOUR portfolio")

""" Setting ticker """
@dp.message_handler(state=PaperFSM.portfolio)
async def paper_setportfolio_getticker(message: types.Message, state: FSMContext):
    await PaperFSM.next()
    await bot.send_message(message.chat.id, "Enter ticker of paper")


""" Checking is ticker on YAHOO """
@dp.message_handler(lambda message: not yahoo.find_ticker(message, new_paper.stock), state=PaperFSM.ticker)
async def noticker_on_yahoo(message: types.Message):
    return await message.reply("Ticker not found")


""" Setting amount """
@dp.message_handler(state=PaperFSM.ticker)
async def paper_setticker_getamount(message: types.Message, state: FSMContext):
    new_paper.ticker = message.text.upper()
    await PaperFSM.next()
    await bot.send_message(message.chat.id, "Enter amount of papers")


""" Setting price """
@dp.message_handler(filters.Regexp(regexp='^-?\d+(?:\.\d+)?$'), state=PaperFSM.amount)
async def paper_setamount_getprice(message: types.Message, state: FSMContext):
    new_paper.amount = message.text
    await PaperFSM.next()
    await bot.send_message(message.chat.id, "Enter price of papers")


""" Chossing currency by keyboard """
@dp.message_handler(filters.Regexp(regexp='^-?\d+(?:\.\d+)?$'), state=PaperFSM.price)
async def paper_setprice_getcurrency(message: types.Message, state: FSMContext):
    new_paper.price = message.text
    await PaperFSM.next()
    await bot.send_message(message.chat.id, "Enter currency")
    # Добавить кнопки выбора валюты


""" Finish FSM, save object to DB """
@dp.message_handler(state=PaperFSM.currency)
async def portfolio_setcurrency_finishmachine(message: types.Message, state: FSMContext):
    new_paper.currency = message.text
    new_paper.save()
    await bot.send_message(message.chat.id, f'Paper has been added to your portfolio\n{new_paper}')
    # Finish conversation
    await state.finish()
