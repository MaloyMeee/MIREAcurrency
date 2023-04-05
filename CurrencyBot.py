from currency_converter import CurrencyConverter
import telebot
from telebot import types

bot = telebot.TeleBot('6192045376:AAExNOAKjTY365h9VKVofI-PAjkOtexwxaw') #токен бота
currency = CurrencyConverter() #запуск библиотеки конвертора
amount = 0


@bot.message_handler(commands=["start"]) #прием сообщения /start
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я умею конвертировать валюту,' #Начальное сообщение на /start
                                      ' если хочешь получить курс пары то введи 1,'
                                      ' в ином случаем пиши сумму для конвертации')
    bot.register_next_step_handler(message, summa) #ловим сумму для конвертации


def summa(message):
    global amount #обьявление amount глобальной
    try: #пробует
        amount = int(message.text.strip()) #из сообщения удаляем пробелы слева и справа, после чего переводим строку в int
    except ValueError: #обработка ошибки на случай если нам прислали не число
        bot.send_message(message.chat.id, 'Неверный ввод! Пробуй ещё')  #ответ на неверное сообщение
        bot.register_next_step_handler(message, summa) #ловим сообщение еще раз
        return

    if amount > 0: #если наша цифра больше нуля, то рисуем в телеграмме кнопки
        markup = types.InlineKeyboardMarkup(row_width=2) #задаем расположение кнопок в 2 столбца
        button1 = types.InlineKeyboardButton('USD/EUR', callback_data='usd/eur') #кнопка с предопределенной валютной парой, отправляем в функцию callback запрос
        button2 = types.InlineKeyboardButton('USD/JPY', callback_data='usd/jpy') #кнопка с предопределенной валютной парой, отправляем в функцию callback запрос
        button3 = types.InlineKeyboardButton('RUB/EUR', callback_data='rub/eur') #кнопка с предопределенной валютной парой, отправляем в функцию callback запрос
        button4 = types.InlineKeyboardButton('RUB/USD', callback_data='rub/usd') #кнопка с предопределенной валютной парой, отправляем в функцию callback запрос
        button5 = types.InlineKeyboardButton('Другое значение', callback_data='else') #кнопка для выбора иной валютной пары отправляем в callback else
        markup.add(button1, button2, button3, button4, button5) #выводим кнопки для пользователя
        bot.send_message(message.chat.id, 'Выберите пару валют', reply_markup=markup) #Выводим сообщение
    else: # если цифра меньше нуля
        bot.send_message(message.chat.id, 'Число должно быть больше нуля! Впиши сумму') #говорим что такое вводить нельзя
        bot.register_next_step_handler(message, summa) #ловим следубщее сообщение


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data != 'else': #если нам прилетело с кнопки название валютной пары
        values = call.data.upper().split('/') #наше значение переводим в верхний регистр и сплитуем по /
        res = currency.convert(amount, values[0], values[1]) # вбиваем в конвертирующую бибилотеку нашу пару и количество денег
        bot.send_message(call.message.chat.id, f'Получилось: {res}. Можете снова вписать сумму') #бот присылает сообщение с тем что получилось
        bot.register_next_step_handler(call.message, summa) #ловим новое сообщение
    else: #если была выбрана кнопка с другим значением валютной пары
        bot.send_message(call.message.chat.id, 'Введите пару значений через "/" ') #бот отправляет сообщение
        bot.register_next_step_handler(call.message, my_currency) #передает сообщение в функцию


def my_currency(message):
    try: #пробует
        values = message.text.upper().split('/') #наше значение переводим в верхний регистр и сплитуем по /
        res = currency.convert(amount, values[0], values[1]) # вбиваем в конвертирующую бибилотеку нашу пару и количество денег
        bot.send_message(message.chat.id, f'Получилось: {round(res,2)}. Можете снова вписать сумму') #бот присылает сообщение с тем что получилось
        bot.register_next_step_handler(message, summa)  #ловим новое сообщение
    except Exception: #ловит ошибку
        bot.send_message(message.chat.id, 'Конвертация не доступна в данный момент, попробуй другую пару') #говорит что такое не может
        bot.register_next_step_handler(message, my_currency) #ловит новое сообщение


bot.polling(none_stop=True) #бесконечный цикл бота
