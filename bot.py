import logging
import aiogram.utils.markdown as md
from aiogram import executor


import handlers
from misc import dp, bot


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    bot.infinity_polling()
