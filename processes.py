import variables
from telebot import types


def send_cycle(user):
    user.button_state = variables.Button.NONE
    variables.last = ""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton(variables.phrase1)
    item2 = types.KeyboardButton(variables.phrase2)
    markup.add(item1, item2)
    variables.bot.send_message(user.user_id, "Что-нибудь ещё?", reply_markup=markup)


def find_user_by_id(user_id):
    for i in variables.ids:
        if i.user_id == user_id:
            return i
    return -1


def get_file_id(subject, number_of_line):
    file = open('photos/' + variables.FolderNames[subject] + '/' + variables.FolderNames[subject] + '.csv', "r")
    return file.read().split("\n")[number_of_line].split(",")[2]


def get_documents_list(index):
    file = open('photos/' + variables.FolderNames[index] + '/' + variables.FolderNames[index] + '.csv', "r")
    lines = file.read().split("\n")
    file.close()
    documents = variables.FolderNames[index] + ":\n\n"
    n = 0
    for line in lines:
        if line != "":
            n += 1
            user_id, first_name, file_id, change_date = line.split(",")
            documents += (str(n) + ". Изменён " + change_date + ". " + first_name + "\n")

    # if len(found_line) != 0:
    #     vars.last = found_line
    #     vars.bot.send_document(user.user_id, found_line.split(",")[1], caption="Изменён " + found_line.split(",")[2])
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     item1 = types.KeyboardButton("Поискать")
    #     item2 = types.KeyboardButton("Не, не надо")
    #     markup.add(item1, item2)
    #     vars.bot.send_message(user.user_id, "Могу поискать ещё. Поискать?", reply_markup=markup)
    # else:
    #     vars.bot.send_message(user.user_id, "Ничего не нашёл :(")
    #     send_cycle(user)

    return [documents, n]


def remove_line_by_id(file, user_id):
    lines_to_save = ""
    for line in file:
        if line.split(",")[0] != user_id and line != '\n':
            lines_to_save += line
    return lines_to_save
