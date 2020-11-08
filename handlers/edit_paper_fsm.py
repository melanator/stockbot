from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from misc import dp, bot
import stock
import messages
import query
import yahoo
from models import Paper
import re
import handlers.keyboard as kb


class PaperEditFSM(StatesGroup):
    amount = State()
    price = State()


class DeletePaperFSM(StatesGroup):
    confirm = State()


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['^\D{1,5}(?:\_\d+){1}$']))
async def ticker_page(message: types.Message, state: FSMContext):
    ticker = re.search(r'[a-zA-Z]{1,5}', message.text).group(0)
    port_id = re.search(r'\d+', message.text).group(0)
    async with state.proxy() as data:
        data['ticker'] = ticker
        data['port_id'] = port_id
    await message.reply(messages.paper(ticker, port_id, message.from_user), reply_markup=kb.paper_kb)


@dp.message_handler(lambda m: m.text in ['Add shares', 'Sell shares'])
async def add_sell_shares(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['command'] = message.text
        if not stock.get_paper(data['ticker'], data['port_id'], message.from_user.id):
            return
    await PaperEditFSM.amount.set()
    answer_message = 'Enter amount of paper. You have: '
    await bot.send_message(message.chat.id, answer_message, reply_markup=kb.cancel_kb)


# Для sell all отдельный хендлер
@dp.message_handler(lambda m: m.text in ['Sell all'])
async def sell_all(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['command'] = message.text
        if not stock.get_paper(data['ticker'], data['port_id'], message.from_user.id):
            return
    await PaperEditFSM.amount.set()
    await PaperEditFSM.next()
    answer_message = 'Enter price'
    await bot.send_message(message.chat.id, answer_message, reply_markup=kb.cancel_kb)


@dp.message_handler(lambda m: m.text.isdigit() or m.text == 'Sell all', state=PaperEditFSM.amount)
async def paper_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = int(message.text)
    await PaperEditFSM.next()
    answer_message = 'Enter price'
    await bot.send_message(message.chat.id, answer_message, reply_markup=kb.cancel_kb)


@dp.message_handler(state=PaperEditFSM.price)
async def portfolio_setcurrency_finishmachine(message: types.Message, state: FSMContext):
    commands = {
        'Add shares': '',
        'Sell shares': '',
        'Sell all': ''
    }
    async with state.proxy() as data:
        data['price'] = int(message.text)
        paper = stock.get_paper(data['ticker'], data['port_id'], message.from_user.id)

        if data['command'] == 'Add shares':
            paper.add_shares(data['amount'], data['price'])
            answer_message = f'Bought {data["amount"]} at price {data["price"]}\n'
            answer_message += messages.paper(data['ticker'], data['port_id'], message.from_user)
        elif data['command'] == 'Sell shares':
            paper.sell_shares(data['amount'], data['price'])
            answer_message = f'Sold {data["amount"]} at price {data["price"]}\n'
            answer_message += messages.paper(data['ticker'], data['port_id'], message.from_user)
        elif data['command'] == 'Sell all':
            paper.sell_all(data['price'])
            paper.delete()
            answer_message = f'Sold all shares at price {data["price"]}\n'
            answer_message += messages.portfolio(data['port_id'])

        await state.finish()
        await bot.send_message(message.chat.id, answer_message, reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(lambda m: m.text in ['Delete position'])
async def delete_paper(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['command'] = message.text
        if not stock.get_paper(data['ticker'], data['port_id'], message.from_user.id):
            return
    await DeletePaperFSM.confirm.set()
    answer_message = 'Delete paper from portfolio. All records will be deleted. \n Use this command only if paper was' \
                     'added by mistake. Confirm your decision'
    await bot.send_message(message.chat.id, answer_message,
                           reply_markup=types.ReplyKeyboardMarkup([['Delete paper', 'Cancel']], resize_keyboard=True))


@dp.message_handler(lambda m: m.text in ['Delete paper'], state=DeletePaperFSM.confirm)
async def confirm_delete(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        paper = stock.get_paper(data['ticker'], data['port_id'], message.from_user.id)
        paper.delete()
        msg = f'Paper deleted \n\n'

        await state.finish()
        await bot.send_message(message.chat.id, msg+messages.portfolio(data['port_id']),
                               reply_markup=types.ReplyKeyboardRemove())
