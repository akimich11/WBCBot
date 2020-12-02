import vars
from telebot import types


def send_cycle(message):
    if find_object_by_user(message.from_user.id) == -1:
        vars.ids.append(vars.UserAnd12(message.from_user.id))
    user_object = find_object_by_user(message.from_user.id)
    user_object.one_or_two = 0
    vars.last = ""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(vars.phrase1)
    item2 = types.KeyboardButton(vars.phrase2)
    markup.add(item1, item2)
    vars.bot.send_message(message.chat.id, "Что-нибудь ещё?", reply_markup=markup)


def find_object_by_user(u_id):
    for i in vars.ids:
        if i.u_id == u_id:
            return i
    return -1


def find_document(message, index, last_line):
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
        vars.bot.send_document(message.chat.id, found_line.split("/")[1], caption="Изменён " + found_line.split("/")[2])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Поискать")
        item2 = types.KeyboardButton("Не, не надо")
        markup.add(item1, item2)
        vars.bot.send_message(message.chat.id, "Могу поискать ещё. Поискать?", reply_markup=markup)
    else:
        vars.bot.send_message(message.chat.id, "Ничего не нашёл :(")
        send_cycle(message)


def remove_line_by_id(file, u_id):
    lines_to_save = ""
    for line in file:
        if line.split("/")[0] != u_id and line != '\n':
            lines_to_save += line
    return lines_to_save
