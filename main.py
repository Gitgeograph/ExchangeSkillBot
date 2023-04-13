import telebot
from config import keys, TOKEN
from extensions import Exchange, APIExeption

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<название валюты>' \
           '<В какую валюту хотите перевести>' \
           '<количество переводимой валюты>\nУвидеть список всех доступных валют: \n/values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIExeption('Слишком много параметров\nВзгляни сюда /help')
        elif len(values) < 3:
            raise APIExeption('Недостаточно параметров\nВзгляни сюда /help')

        quote, base, amount = values
        total_base = Exchange.get_price(base, quote, amount)
    except APIExeption as e:
        bot.reply_to(message, f'Ошибка пользователя: \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = (f'Цена {amount} {keys[quote.lower()]} в {keys[base.lower()]} = {total_base}')
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)