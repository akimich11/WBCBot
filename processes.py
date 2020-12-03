import vars
from telebot import types


def send_cycle(user):
    user.button_state = vars.Button.NONE
    vars.last = ""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(vars.phrase1)
    item2 = types.KeyboardButton(vars.phrase2)
    markup.add(item1, item2)
    vars.bot.send_message(user.user_id, "Что-нибудь ещё?", reply_markup=markup)


def find_object_by_user(user_id):
    for i in vars.ids:
        if i.user_id == user_id:
            return i
    return -1


def find_document(user, index, last_line):
    file = open('photos/' + vars.FolderNames[index] + '/' + vars.FolderNames[index] + '.txt', "r")
    found_line = ""
    for line in file:
        if line == last_line:
            break
        elif line != "\n":
            found_line = line
    file.close()

    if len(found_line) != 0:
        vars.last = found_line
        vars.saved_index = index
        vars.bot.send_document(user.user_id, found_line.split("/")[1], caption="Изменён " + found_line.split("/")[2])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Поискать")
        item2 = types.KeyboardButton("Не, не надо")
        markup.add(item1, item2)
        vars.bot.send_message(user.user_id, "Могу поискать ещё. Поискать?", reply_markup=markup)
    else:
        vars.bot.send_message(user.user_id, "Ничего не нашёл :(")
        send_cycle(user)


def remove_line_by_id(file, user_id):
    lines_to_save = ""
    for line in file:
        if line.split("/")[0] != user_id and line != '\n':
            lines_to_save += line
    return lines_to_save
