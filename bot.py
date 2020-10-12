import telebot
import os
import glob
import pytz
import datetime
from PIL import Image
from telebot import types

bot = telebot.TeleBot('1165511829:AAFV6MBiSUdIbxr6GVQ51B01Qhm9vz2psF4', threaded=False)

ids = []
photos = []
phrase1 = "Скатать дз"
phrase2 = "Скинуть тетрадку"
user = ""
user_id = ""
last = ""
saved_index = -1
FolderNames = [
    "МА практика",
    "ДУ практика",
    "ДМиМЛ практика",
    "ВМА практика",
    "МА конспект",
    "ДУ конспект",
    "ДМиМЛ конспект",
    "ВМА конспект"]


class UserAnd12:
    def __init__(self, u_id):
        self.u_id = u_id
        self.one_or_two = 0


if __name__ == '__main__':
    bot.send_message(270241310, "перезагрузился")


def remove_line_by_id(file, u_id):
    lines_to_save = ""
    for line in file:
        if line.split("/")[0] != u_id and line != '\n':
            lines_to_save += line
    return lines_to_save


def find_object_by_user(u_id):
    for i in ids:
        if i.u_id == u_id:
            return i
    return -1


def send_cycle(message):
    global last
    if find_object_by_user(message.from_user.id) == -1:
        ids.append(UserAnd12(message.from_user.id))
    user_object = find_object_by_user(message.from_user.id)
    user_object.one_or_two = 0
    last = ""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(phrase1)
    item2 = types.KeyboardButton(phrase2)
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Что-нибудь ещё?", reply_markup=markup)


def find_document(message, index, last_line):
    file = open('photos/' + FolderNames[index] + '/' + FolderNames[index] + '.txt', "r")
    found_line = ""
    for line in file:
        if line == last_line:
            break
        elif line != "\n":
            found_line = line
    file.close()

    if len(found_line) != 0:
        global last, saved_index
        last = found_line
        saved_index = index
        bot.send_document(message.chat.id, found_line.split("/")[1], caption="Изменён " + found_line.split("/")[2])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Поискать")
        item2 = types.KeyboardButton("Не, не надо")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, "Могу поискать ещё. Поискать?", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Ничего не нашёл :(")
        send_cycle(message)


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

    markup.add(item1, item2, item3, item4, item5, item6, item7, item8)
    bot.send_message(message.chat.id, 'Из какой тетрадки?', reply_markup=markup)


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(phrase1)
    item2 = types.KeyboardButton(phrase2)
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Привет. Я бот. Буду организовывать обмен тетрадками между вами. "
                                      "Работаю по принципу буккроссинга: можно брать тетрадки, можно делиться ими. "
                                      "Надеюсь, понятно, что если никто не будет делиться тетрадками, то и брать"
                                      " будет нечего. Так что надеюсь на вашу совесть")
    bot.send_message(message.chat.id, "Что ты хочешь сделать?", reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def append_photo(message):
    global photos
    if find_object_by_user(message.from_user.id) == -1:
        ids.append(UserAnd12(message.from_user.id))
    find_object_by_user(message.from_user.id).one_or_two = 2
    photos.append(message.photo[-1].file_id)


@bot.message_handler(content_types=['text'])
def reply(message):
    global user_id, last, photos
    if find_object_by_user(message.from_user.id) == -1:
        ids.append(UserAnd12(message.from_user.id))
    user_object = find_object_by_user(message.from_user.id)

    if message.text == phrase1:
        user_id = message.from_user.id
        user_object.one_or_two = 1
        create_markup(message)

    elif message.text == phrase2:
        user_object.one_or_two = 2
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("готово")
        item2= types.KeyboardButton("отмена")
        markup.add(item1, item2)
        bot.send_message(message.chat.id,
                         'Тогда просто кидай фотки, а я сделаю всё остальное.' +
                         ' Когда все фотки загрузятся, нажми кнопку "готово"',
                         reply_markup=markup)

    elif message.text == "готово":
        global user
        if len(photos) == 0:
            bot.send_message(message.chat.id, "Сначала скинь фотки")
        else:
            user = message.from_user.first_name
            user_id = message.from_user.id
            create_markup(message)

    elif message.text == "Поискать":
        global saved_index
        find_document(message, saved_index, last)

    elif message.text == "Не, не надо" or message.text == "отмена":
        photos.clear()
        send_cycle(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        global user_id
        if find_object_by_user(user_id) == -1:
            ids.append(UserAnd12(user_id))
        user_object = find_object_by_user(user_id)
        index = int(call.data) - 1
        idx = 1

        if user_object.one_or_two == 2:
            global photos, user
            im_list = []
            parent_dir = 'photos/' + FolderNames[index]
            directory = str(user_id)
            path = os.path.join(parent_dir, directory)
            if not os.path.isdir(path):
                os.mkdir(path)
            else:
                jpg_list = glob.glob(path + '/*.jpg')
                max_el = 0
                for i in jpg_list:
                    a = int((i.split("/")[-1]).split(".")[0])
                    if a > max_el:
                        max_el = a
                idx = max_el + 1

            for j in photos:
                my_photo = bot.get_file(j)
                filename, file_extension = os.path.splitext(my_photo.file_path)
                src = 'photos/' + FolderNames[index] + '/' + directory + '/' + str(idx) + file_extension
                idx += 1
                with open(src, "wb") as new_file:
                    new_file.write(bot.download_file(my_photo.file_path))
                new_file.close()
            photos.clear()
            im1 = Image.open("photos/" + FolderNames[index] + '/' + directory + "/1.jpg")
            for i in range(2, idx):
                im_list.append(Image.open("photos/" + FolderNames[index] + '/' + directory + '/' + str(i) + ".jpg"))
            pdf1_filename = "photos/" + FolderNames[index] + '/' + directory + '/' + \
                            FolderNames[index] + "_" + user + ".pdf"
            im1.save(pdf1_filename, "PDF", resolution=100.0, save_all=True, append_images=im_list)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Фотографии добавлены", reply_markup=None)
            doc = bot.send_document(call.message.chat.id, open(pdf1_filename, "rb"))

            f = open('photos/' + FolderNames[index] + '/' + FolderNames[index] + '.txt', 'r')
            lines = remove_line_by_id(f, str(user_id))
            f.close()
            f = open('photos/' + FolderNames[index] + '/' + FolderNames[index] + '.txt', 'w')
            tz = pytz.timezone('Europe/Minsk')
            now = datetime.datetime.now(tz)
            f.write(lines + str(user_id) + '/' + doc.document.file_id + '/' + now.strftime("%d-%m-%Y в %H:%M") + '\n')
            f.close()
            send_cycle(call.message)

        elif user_object.one_or_two == 1:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Ок ща поищу", reply_markup=None)
            last_line = ""
            find_document(call.message, index, last_line)


bot.polling(none_stop=True)
