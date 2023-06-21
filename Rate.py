import telebot
from config import keys, TOKEN
from utils import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

#Вывод сообщения с инструкцией работы м конвертером
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Увидеть список доступных валют:/values.\nЧтобы начать работу, введите команду в следующем формате:\n<название конвертируемой валюты> \
<в какую валюту перевести> \
<сумма конвертации>\nВАЖНО: Указывайте название валют\nв **ЕДИНСТВЕННОМ ЧИСЛЕ!**'
    bot.reply_to(message, text)

#Вывод наименования имеющихся валют
@bot.message_handler(commands=['values'])
def value_info(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

#Ввод информации от пользователя бота и перевод валют
@bot.message_handler(content_types=['text', ])
def convert_info(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Введено слмшком много параметров.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} равна {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)