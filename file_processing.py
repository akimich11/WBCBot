import variables as v
import pytz
import datetime


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


def save_lines(student_files, pdfs_to_write):
    line_number = 0
    lines_to_save = ""
    try:
        with open(student_files, encoding='utf-8') as f:
            files_len = int(len(f.read().split("\n")))
            iterations = files_len - pdfs_to_write
            for line in f:
                line_number += 1
                if line_number > iterations:
                    break
                lines_to_save += line + "\n"
    except FileNotFoundError:
        pass
    return lines_to_save


def write_pdf_id(user, subject_id, docs, pdfs_to_write):
    directory = 'photos' + v.DEL + v.folders[subject_id]
    subject_database = directory + v.DEL + v.folders[subject_id] + '.csv'
    with open(subject_database, 'r', encoding='utf-8') as f:
        lines = remove_line_by_id(f, str(user.user_id))
    with open(subject_database, 'w', encoding='utf-8') as f:
        tz = pytz.timezone('Europe/Minsk')
        now = datetime.datetime.now(tz)
        f.write(lines + str(user.user_id) + ',' + user.first_name + ',' + now.strftime("%d-%m-%Y  %H:%M") + '\n')

    student_files = directory + v.DEL + str(user.user_id) + v.DEL + user.first_name + '.txt'
    lines = save_lines(student_files, pdfs_to_write)
    with open(student_files, "w", encoding='utf-8') as f:
        f.write(lines)
        for doc in docs:
            f.write(doc.document.file_id + '\n')
