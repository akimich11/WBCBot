import processes
import vars
from analyser import analyse
from telebot import types


if __name__ == '__main__':
    vars.bot.send_message(270241310, "перезагрузился")


def create_markup(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("МА практика", callback_data='1')
    item2 = types.InlineKeyboardButton("ДУ практика", callback_data='2')
    item3 = types.InlineKeyboardButton("ДМиМЛ практика", callback_data='3')
    item4 = types.InlineKeyboardButton("ВМА практика", callback_data='4')
    item5 = types.InlineKeyboardButton("МА конспект", callback_data='5')
    item6 = types.InlineKeyboardButton("ДУ конспект", callback_data='6')
    item7 = types.InlineKeyboardButton("ДМиМЛ конспект", callback_data='7')
    item8 = types.InlineKeyboardButton("ВМА конспект", callback_data='8')
    item9 = types.InlineKeyboardButton("Другое", callback_data='9')

    markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9)
    vars.bot.send_message(message.chat.id, 'Из какой тетрадки?', reply_markup=markup)


@vars.bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(vars.phrase1)
    item2 = types.KeyboardButton(vars.phrase2)
    markup.add(item1, item2)
    vars.bot.send_message(message.chat.id, "Привет. Я бот. Буду организовывать обмен тетрадками между вами. "
                                           "Работаю по принципу буккроссинга: можно брать тетрадки, можно делиться ими."
                                           " Надеюсь, понятно, что если никто не будет делиться тетрадками, то и брать"
                                           " будет нечего. Так что надеюсь на вашу совесть")
    vars.bot.send_message(message.chat.id, "Что ты хочешь сделать?", reply_markup=markup)


@vars.bot.message_handler(content_types=['photo'])
def append_photo(message):
    if processes.find_object_by_user(message.from_user.id) == -1:
        vars.ids.append(vars.UserAnd12(message.from_user.id))
    processes.find_object_by_user(message.from_user.id).one_or_two = 2
    vars.photos.append(message.photo[-1].file_id)


@vars.bot.message_handler(content_types=['text'])
def reply(message):
    if processes.find_object_by_user(message.from_user.id) == -1:
        vars.ids.append(vars.UserAnd12(message.from_user.id))
    user_object = processes.find_object_by_user(message.from_user.id)

    if message.text == vars.phrase1:
        vars.user_id = message.from_user.id
        user_object.one_or_two = 1
        create_markup(message)

    elif message.text == vars.phrase2:
        user_object.one_or_two = 2
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("готово")
        item2 = types.KeyboardButton("отмена")
        markup.add(item1, item2)
        vars.bot.send_message(message.chat.id,
                              'Тогда просто кидай фотки, а я сделаю всё остальное.' +
                              ' Когда все фотки загрузятся, нажми кнопку "готово"',
                              reply_markup=markup)

    elif message.text == "готово":
        if len(vars.photos) == 0:
            vars.bot.send_message(message.chat.id, "Сначала скинь фотки")
        else:
            vars.user = message.from_user.first_name
            vars.user_id = message.from_user.id
            create_markup(message)

    elif message.text == "Поискать":
        processes.find_document(message, vars.saved_index, vars.last)

    elif message.text == "Не, не надо" or message.text == "отмена":
        vars.photos.clear()
        processes.send_cycle(message)


@vars.bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        analyse(call.message, call.data)


vars.bot.polling(none_stop=True)
