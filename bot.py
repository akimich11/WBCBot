import pdf_maker as pdf
import file_processing as file
import variables as v
from telebot import types

if __name__ == '__main__':
    v.bot.send_message(270241310, "перезагрузился")


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
    v.bot.send_message(message.chat.id, 'Из какой тетрадки?', reply_markup=markup)


def send_cycle(user):
    user.button_state = v.Button.NONE
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(v.phrase1)
    item2 = types.KeyboardButton(v.phrase2)
    markup.add(item1, item2)
    v.bot.send_message(user.user_id, "Что-нибудь ещё?", reply_markup=markup)


@v.bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(v.phrase1)
    item2 = types.KeyboardButton(v.phrase2)
    markup.add(item1, item2)
    with open("changelog.txt", encoding='utf-8') as f:
        v.bot.send_message(message.chat.id, "Привет, я бот с тетрадками, версия 2.0.\n"
                                            "Вот изменилось по сравнению с предыдущей версией:\n\n" + f.read())
    v.bot.send_message(message.chat.id, "Что ты хочешь сделать?", reply_markup=markup)


@v.bot.message_handler(commands=['users'])
def send_users(message):
    if message.from_user.id == 270241310:
        s = "Список пользователей бота:\n\n"
        for user in v.users:
            if user.username is not None:
                s += str(user.user_id) + " " + user.first_name + " " + str(user.last_name) + " @" + user.username + "\n"
            else:
                s += str(user.user_id) + " " + user.first_name + " " + str(user.last_name) + "\n"
        v.bot.send_message(message.chat.id, s)


@v.bot.message_handler(content_types=['photo'])
def append_photo(message):
    user = file.get_user(message)
    user.photos.append(message.photo[-1].file_id)


@v.bot.message_handler(content_types=['document'])
def append_file(message):
    user = file.get_user(message)
    extension = message.document.file_name.split(".")[1]
    if extension.lower() in v.accepted_formats:
        user.files.append(message.document.file_id)
    else:
        v.bot.send_message(message.chat.id, "Расширение файла (" + extension + ") не поддерживается")


@v.bot.message_handler(content_types=['text'])
def reply(message):
    user = file.get_user(message)

    if message.text == v.phrase1:
        user.button_state = v.Button.FIND
        create_markup(message)

    elif message.text == v.phrase2:
        user.button_state = v.Button.SEND
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("готово")
        item2 = types.KeyboardButton("отмена")
        markup.add(item1, item2)
        v.bot.send_message(message.chat.id,
                           'Тогда просто кидай фотки, а я сделаю всё остальное.' +
                           ' Когда все фотки загрузятся, нажми кнопку "готово"',
                           reply_markup=markup)

    elif message.text == "готово":
        if len(user.photos) == 0 and len(user.files) == 0:
            v.bot.send_message(message.chat.id, "Сначала скинь фотки")
        else:
            create_markup(message)

    elif message.text == "отмена":
        user.photos.clear()
        user.files.clear()
        user.subject_id = -1
        send_cycle(user)

    elif user.subject_id != -1:
        key = int(message.text)
        files = file.get_file_id(user.subject_id, key - 1)
        if len(files) > 1:
            input_documents = []
            for file_id in files:
                input_documents.append(types.InputMediaDocument(file_id))
            groups = [input_documents[i: i + 10] for i in range(0, len(input_documents), 10)]
            for group in groups:
                v.bot.send_media_group(user.user_id, group)
        elif len(files) == 1:
            v.bot.send_document(user.user_id, files[0])
        user.subject_id = -1
        send_cycle(user)


@v.bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        user = file.get_user(call)
        button_index = int(call.data) - 1

        if user.button_state == v.Button.SEND:
            v.bot.edit_message_text("Идёт загрузка фотографий...", user.user_id, call.message.message_id,
                                    reply_markup=None)
            old_index, new_index = pdf.update_photos(user, button_index)
            v.bot.edit_message_text("Идёт создание pdf...", user.user_id, call.message.message_id)
            filenames = pdf.create_pdf(user, button_index, old_index, new_index)
            v.bot.edit_message_text("Тетрадка загружена", user.user_id, call.message.message_id)
            docs = []
            for filename in filenames:
                docs.append(v.bot.send_document(call.message.chat.id, open(filename, "rb")))
            file.write_pdf_id(docs, user, button_index, old_index)
            send_cycle(user)

        elif user.button_state == v.Button.FIND:
            v.bot.edit_message_text(chat_id=user.user_id, message_id=call.message.message_id,
                                    text="Ок ща поищу", reply_markup=None)

            docs, lines_number = file.get_documents_list(button_index)
            items = ["отмена"]
            for i in range(lines_number):
                items.append(str(i + 1))
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
            markup.add(*items)
            v.bot.send_message(user.user_id, "Вот что у меня есть по предмету " + docs + "\nЧто тебе нужно?",
                               reply_markup=markup)
            user.subject_id = button_index


v.bot.polling(none_stop=True)
