import pdf_maker
import processes
import vars
from telebot import types


if __name__ == '__main__':
    vars.bot.send_message(270241310, "перезагрузился")


def create_markup(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    user_data = str(message.from_user.id) + "/" + message.from_user.first_name + "/"
    item1 = types.InlineKeyboardButton("МА практика",    callback_data=user_data + '1')
    item2 = types.InlineKeyboardButton("ДУ практика",    callback_data=user_data + '2')
    item3 = types.InlineKeyboardButton("ДМиМЛ практика", callback_data=user_data + '3')
    item4 = types.InlineKeyboardButton("ВМА практика",   callback_data=user_data + '4')
    item5 = types.InlineKeyboardButton("МА конспект",    callback_data=user_data + '5')
    item6 = types.InlineKeyboardButton("ДУ конспект",    callback_data=user_data + '6')
    item7 = types.InlineKeyboardButton("ДМиМЛ конспект", callback_data=user_data + '7')
    item8 = types.InlineKeyboardButton("ВМА конспект",   callback_data=user_data + '8')
    item9 = types.InlineKeyboardButton("Другое",         callback_data=user_data + '9')

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
        vars.ids.append(vars.User(message.from_user.id, message.from_user.first_name))
    user = processes.find_object_by_user(message.from_user.id)
    user.photos.append(message.photo[-1].file_id)


@vars.bot.message_handler(content_types=['text'])
def reply(message):
    if processes.find_object_by_user(message.from_user.id) == -1:
        vars.ids.append(vars.User(message.from_user.id, message.from_user.first_name))
    user = processes.find_object_by_user(message.from_user.id)

    if message.text == vars.phrase1:
        user.button_state = vars.Button.FIND
        create_markup(message)

    elif message.text == vars.phrase2:
        user.button_state = vars.Button.SEND
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("готово")
        item2 = types.KeyboardButton("отмена")
        markup.add(item1, item2)
        vars.bot.send_message(message.chat.id,
                              'Тогда просто кидай фотки, а я сделаю всё остальное.' +
                              ' Когда все фотки загрузятся, нажми кнопку "готово"',
                              reply_markup=markup)

    elif message.text == "готово":
        if len(user.photos) == 0:
            vars.bot.send_message(message.chat.id, "Сначала скинь фотки")
        else:
            create_markup(message)

    elif message.text == "Поискать":
        processes.find_document(user, vars.saved_index, vars.last)

    elif message.text == "Не, не надо" or message.text == "отмена":
        user.photos.clear()
        processes.send_cycle(user)


@vars.bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        user_id, first_name, number = call.data.split("/")
        if processes.find_object_by_user(int(user_id)) == -1:
            vars.ids.append(vars.User(user_id, first_name))
        user = processes.find_object_by_user(int(user_id))
        button_index = int(number) - 1

        if user.button_state == vars.Button.SEND:
            idx = pdf_maker.download_photos(user, button_index)
            filename = pdf_maker.create_pdf(user, button_index, idx)
            vars.bot.edit_message_text(chat_id=user.user_id, message_id=call.message.message_id,
                                       text="Фотографии добавлены", reply_markup=None)
            doc = vars.bot.send_document(call.message.chat.id, open(filename, "rb"))
            pdf_maker.write_pdf_id(user, button_index, doc)
            processes.send_cycle(user)

        elif user.button_state == vars.Button.FIND:
            vars.bot.edit_message_text(chat_id=user.user_id, message_id=call.message.message_id,
                                       text="Ок ща поищу", reply_markup=None)
            last_line = ""
            processes.find_document(user, button_index, last_line)


vars.bot.polling(none_stop=True)
