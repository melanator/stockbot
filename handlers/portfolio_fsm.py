from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types
from misc import dp, bot
import stock


# Bunch of handlers to create new portfolio. Needs to move out. 
class PortfolioFSM(StatesGroup):
    portfolio = State()
    broker = State()
    margin = State()


@dp.message_handler(commands=['newportfolio'])
async def new_portfolio(message: types.Message):
    await PortfolioFSM.portfolio.set()
    await message.reply("Enter name of portfolio")


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
    # And remove keyboard (just in case)
    await message.reply('Portfolio creating has been cancelled.')


@dp.message_handler(state=PortfolioFSM.portfolio)
async def portfolio_setportfolio_getbroker(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['portfolio'] = message.text
    await PortfolioFSM.next()
    await message.reply("Enter name of your broker")


@dp.message_handler(state=PortfolioFSM.broker)
async def portfolio_setbroker_getmargin(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['broker'] = message.text
    await PortfolioFSM.next()
    await message.reply("Enter your margin")


@dp.message_handler(state=PortfolioFSM.margin)
async def portfolio_setmargin_finishstates(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['margin'] = message.text

        # Add entry
        stock.create_portfolio(data['portfolio'],
                               data['broker'],
                               data['margin'],
                               message.from_user.id)
    await bot.send_message(message.chat.id, 'Portfolio has been added')
    # Finish conversation
    await state.finish()
