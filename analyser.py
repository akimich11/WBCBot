import processes
import vars
import os
import glob
import pytz
import datetime
from PIL import Image


def analyse(message, data):
    if processes.find_object_by_user(vars.user_id) == -1:
        vars.ids.append(vars.UserAnd12(vars.user_id))
    user_object = processes.find_object_by_user(vars.user_id)
    index = int(data) - 1
    idx = 1

    if user_object.one_or_two == 2:
        im_list = []
        parent_dir = 'photos/' + vars.FolderNames[index]
        directory = str(vars.user_id)
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

        for j in vars.photos:
            my_photo = vars.bot.get_file(j)
            filename, file_extension = os.path.splitext(my_photo.file_path)
            src = 'photos/' + vars.FolderNames[index] + '/' + directory + '/' + str(idx) + file_extension
            idx += 1
            with open(src, "wb") as new_file:
                new_file.write(vars.bot.download_file(my_photo.file_path))
            new_file.close()
        vars.photos.clear()
        im1 = Image.open("photos/" + vars.FolderNames[index] + '/' + directory + "/1.jpg")
        for i in range(2, idx):
            im_list.append(
                Image.open("photos/" + vars.FolderNames[index] + '/' + directory + '/' + str(i) + ".jpg"))
        pdf1_filename = "photos/" + vars.FolderNames[index] + '/' + directory + '/' + \
                        vars.FolderNames[index] + "_" + vars.user + ".pdf"
        im1.save(pdf1_filename, "PDF", resolution=100.0, save_all=True, append_images=im_list)
        vars.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                   text="Фотографии добавлены", reply_markup=None)
        doc = vars.bot.send_document(message.chat.id, open(pdf1_filename, "rb"))

        f = open('photos/' + vars.FolderNames[index] + '/' + vars.FolderNames[index] + '.txt', 'r')
        lines = processes.remove_line_by_id(f, str(vars.user_id))
        f.close()
        f = open('photos/' + vars.FolderNames[index] + '/' + vars.FolderNames[index] + '.txt', 'w')
        tz = pytz.timezone('Europe/Minsk')
        now = datetime.datetime.now(tz)
        f.write(lines + str(vars.user_id) + '/' + doc.document.file_id + '/' + now.strftime("%d-%m-%Y в %H:%M") +
                '\n')
        f.close()
        processes.send_cycle(message)

    elif user_object.one_or_two == 1:
        vars.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                   text="Ок ща поищу", reply_markup=None)
        last_line = ""
        processes.find_document(message, index, last_line)
