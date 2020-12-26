import variables as v
import pytz
import datetime


def bisect(a, x, lo=0):
    hi = len(a)
    if hi == 0:
        return -1
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid].user_id < x:
            lo = mid + 1
        else:
            hi = mid
    return lo


def get_user(message):
    index = bisect(v.users, message.from_user.id)
    try:
        return v.users[index]
    except IndexError:
        user = v.User(message)
        v.users.insert(index, user)
        return user


def get_file_id(subject, number_of_line):
    directory = 'photos' + v.DEL + v.folders[subject] + v.DEL
    file = open(directory + v.folders[subject] + '.csv', encoding='utf-8')
    file_data = file.read()
    file.close()
    id_list = []
    try:
        user_id = file_data.split("\n")[number_of_line].split(",")[0]
        with open(directory + user_id + v.DEL + user_id + ".txt") as file:
            id_list = file.read().split("\n")
        id_list.remove("")
    except IndexError:
        pass
    return id_list


def get_documents_list(subject):
    file = open('photos' + v.DEL + v.folders[subject] + v.DEL + v.folders[subject] + '.csv', encoding='utf-8')
    lines = file.read().split("\n")
    file.close()
    documents = v.folders[subject] + ":\n\n"
    n = 0
    for line in lines:
        if line != "":
            n += 1
            user_id, first_name, change_date = line.split(",")
            documents += (str(n) + ". Изменён " + change_date + ". " + first_name + "\n")
    return [documents, n]


def remove_line_by_id(filename, user_id):
    lines_to_save = ""
    try:
        with open(filename, encoding='utf-8') as f:
            lines = f.read().split("\n")
        for line in lines:
            if line.split(",")[0] != user_id and line != '':
                lines_to_save += line + "\n"
    except FileNotFoundError:
        pass
    return lines_to_save


def remove_last_line(filename):
    line_number = 0
    lines_to_save = ""
    try:
        with open(filename, encoding='utf-8') as f:
            lines = f.read().split("\n")
        for line in lines:
            line_number += 1
            if line_number > len(lines) - 2:
                break
            lines_to_save += line + "\n"
    except FileNotFoundError:
        pass
    return lines_to_save


def write_pdf_id(docs, user, subject_id, old_index):
    directory = 'photos' + v.DEL + v.folders[subject_id] + v.DEL
    subject_database = directory + v.folders[subject_id] + '.csv'
    lines = remove_line_by_id(subject_database, str(user.user_id))
    with open(subject_database, 'w', encoding='utf-8') as f:
        tz = pytz.timezone('Europe/Minsk')
        now = datetime.datetime.now(tz)
        f.write(lines + str(user.user_id) + ',' + user.first_name + ',' + now.strftime("%d.%m.%Y в %H:%M") + '\n')

    student_files = directory + str(user.user_id) + v.DEL + user.first_name + '.txt'
    if old_index % 20 != 1:
        lines = remove_last_line(student_files)
        f = open(student_files, "w", encoding='utf-8')
        f.write(lines)
    else:
        f = open(student_files, "a", encoding='utf-8')
    for doc in docs:
        f.write(doc.document.file_id + '\n')
    f.close()
