import telebot
from telebot import types
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    message_text = f'Привет {message.chat.first_name}, ты написал мне /start.'
    bot.send_message(message.chat.id, message_text)


@bot.message_handler(commands=["portfolio"])
def portfolio(message):
    # Эти параметры для клавиатуры необязательны, просто для удобства
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard.add(button_phone)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id, "Выберите портфель или добавьте новый /newportfolio", reply_markup=keyboard) 

'''
Возвращает 
'''
@bot.message_handler(content_types=["text"])
def repeat_all_messages(message): # Название функции не играет никакой роли
    bot.send_message(message.chat.id, message.text)   

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
    bot.infinity_polling()
