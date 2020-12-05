import variables as v
from telebot import types


def send_cycle(user):
    user.button_state = v.Button.NONE
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(v.phrase1)
    item2 = types.KeyboardButton(v.phrase2)
    markup.add(item1, item2)
    v.bot.send_message(user.user_id, "Что-нибудь ещё?", reply_markup=markup)


def get_user(message):
    for i in v.users:
        if i.user_id == message.from_user.id:
            return i
    user = v.User(message.from_user.id, message.from_user.first_name)
    v.users.append(user)
    return user


def get_file_id(subject, number_of_line):
    file = open('photos' + v.DEL + v.folders[subject] + v.DEL + v.folders[subject] + '.csv', "r", encoding='utf-8')
    file_data = file.read()
    file.close()
    return file_data.split("\n")[number_of_line].split(",")[2]


def get_documents_list(index):
    file = open('photos' + v.DEL + v.folders[index] + v.DEL + v.folders[index] + '.csv', "r", encoding='utf-8')
    lines = file.read().split("\n")
    file.close()
    documents = v.folders[index] + ":\n\n"
    n = 0
    for line in lines:
        if line != "":
            n += 1
            user_id, first_name, file_id, change_date = line.split(",")
            documents += (str(n) + ". Изменён " + change_date + ". " + first_name + "\n")
    return [documents, n]


def remove_line_by_id(file, user_id):
    lines_to_save = ""
    for line in file:
        if line.split(",")[0] != user_id and line != '\n':
            lines_to_save += line
    return lines_to_save
