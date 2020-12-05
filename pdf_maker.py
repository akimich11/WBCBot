import processes as proc
import variables as v
import os
import glob
import pytz
import datetime
from PIL import Image


def download_files(file_ids, directory, idx):
    for f_id in file_ids:
        file_to_save = v.bot.get_file(f_id)
        file_extension = os.path.splitext(file_to_save.file_path)[1]
        filename = directory + v.DEL + str(idx) + file_extension.lower()
        idx += 1
        with open(filename, "wb") as new_file:
            new_file.write(v.bot.download_file(file_to_save.file_path))
    file_ids.clear()
    return idx


def update_photos(user, subject_id):
    idx = 1
    parent_dir = 'photos' + v.DEL + v.folders[subject_id]
    directory = str(user.user_id)
    path = os.path.join(parent_dir, directory)
    if not os.path.isdir(path):
        os.mkdir(path)
    else:
        jpg_list = glob.glob(path + v.DEL + '*.jpg')
        jpg_list += glob.glob(path + v.DEL + '*.jpeg')
        jpg_list += glob.glob(path + v.DEL + '*.png')
        max_el = 0
        for i in jpg_list:
            a = int((i.split(v.DEL)[-1]).split(".")[0])
            if a > max_el:
                max_el = a
        idx = max_el + 1
    directory = parent_dir + v.DEL + directory
    idx = download_files(user.photos, directory, idx)
    return download_files(user.files, directory, idx)


def open_image(filename):
    try:
        temp = Image.open(filename + ".jpg")
    except FileNotFoundError:
        try:
            temp = Image.open(filename + ".png")
            temp = temp.convert('RGB')
        except FileNotFoundError:
            temp = Image.open(filename + ".jpeg")
    image = temp.copy()
    temp.close()
    return image


def create_pdf(user, subject_id, idx):
    im_list = []
    pdf_list = []
    directory = 'photos' + v.DEL + v.folders[subject_id] + v.DEL + str(user.user_id)
    iterations = int(idx / 20) + 1
    for i in range(iterations):
        im1 = open_image(directory + v.DEL + str(20 * i + 1))
        j = 2
        while j < 21:
            page_number = 20 * i + j
            if page_number > idx - 1:
                break
            im_list.append(open_image(directory + v.DEL + str(page_number)))
            j += 1
        pdf_filename = directory + v.DEL + v.folders[subject_id] + "_" + user.first_name + "_" + str(i + 1) + ".pdf"
        im1.save(pdf_filename, "PDF", resolution=100.0, save_all=True, append_images=im_list)
        pdf_list.append(pdf_filename)
        im1.close()
        im_list.clear()
    return pdf_list


def write_pdf_id(user, subject_id, doc):
    filename = 'photos' + v.DEL + v.folders[subject_id] + v.DEL + v.folders[subject_id] + '.csv'
    f = open(filename, 'r', encoding='utf-8')
    lines = proc.remove_line_by_id(f, str(user.user_id))
    f.close()
    f = open(filename, 'w', encoding='utf-8')
    tz = pytz.timezone('Europe/Minsk')
    now = datetime.datetime.now(tz)
    f.write(lines + str(user.user_id) + ',' + user.first_name + "," + doc.document.file_id + ',' +
            now.strftime("%d-%m-%Y  %H:%M") + '\n')
    f.close()
