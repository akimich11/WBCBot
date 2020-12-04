import processes
import variables as v
import os
import glob
import pytz
import datetime
from PIL import Image


def download_files(files, directory, button_index, idx):
    for j in files:
        my_photo = v.bot.get_file(j)
        filename, file_extension = os.path.splitext(my_photo.file_path)
        src = 'photos' + v.DEL + v.FolderNames[button_index] + v.DEL + directory + v.DEL + str(idx) + file_extension
        idx += 1
        with open(src, "wb") as new_file:
            new_file.write(v.bot.download_file(my_photo.file_path))
        new_file.close()
    files.clear()
    return idx


def download(user, button_index):
    idx = 1
    parent_dir = 'photos' + v.DEL + v.FolderNames[button_index]
    directory = str(user.user_id)
    path = os.path.join(parent_dir, directory)
    if not os.path.isdir(path):
        os.mkdir(path)
    else:
        jpg_list = glob.glob(path + v.DEL + '*.jpg')
        max_el = 0
        for i in jpg_list:
            a = int((i.split(v.DEL)[-1]).split(".")[0])
            if a > max_el:
                max_el = a
        idx = max_el + 1
    idx = download_files(user.photos, directory, button_index, idx)
    idx = download_files(user.files, directory, button_index, idx)
    return idx


def create_pdf(user, button_index, idx):
    im_list = []
    directory = str(user.user_id)
    im1 = Image.open('photos' + v.DEL + v.FolderNames[button_index] + v.DEL + directory + v.DEL + "1.jpg")
    for i in range(idx - 2):
        im_list.append(
            Image.open('photos' + v.DEL + v.FolderNames[button_index] + v.DEL + directory + v.DEL + str(i + 2) + ".jpg"))
    pdf1_filename = 'photos' + v.DEL + v.FolderNames[button_index] + v.DEL + directory + v.DEL + \
                    v.FolderNames[button_index] + "_" + user.first_name + ".pdf"
    im1.save(pdf1_filename, "PDF", resolution=100.0, save_all=True, append_images=im_list)
    return pdf1_filename


def write_pdf_id(user, button_index, doc):
    f = open('photos' + v.DEL + v.FolderNames[button_index] + v.DEL + v.FolderNames[button_index] + '.csv', 'r')
    lines = processes.remove_line_by_id(f, str(user.user_id))
    f.close()
    f = open('photos' + v.DEL + v.FolderNames[button_index] + v.DEL + v.FolderNames[button_index] + '.csv', 'w')
    tz = pytz.timezone('Europe/Minsk')
    now = datetime.datetime.now(tz)
    f.write(lines + str(user.user_id) + ',' + user.first_name + "," + doc.document.file_id + ',' +
            now.strftime("%d-%m-%Y  %H:%M") + '\n')
    f.close()
