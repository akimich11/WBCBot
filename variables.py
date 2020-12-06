import telebot
from enum import Enum

bot = telebot.TeleBot('1165511829:AAFV6MBiSUdIbxr6GVQ51B01Qhm9vz2psF4', threaded=False)
users = []
DEL = '/'
phrase1 = "Найти дз"
phrase2 = "Отправить тетрадку"
accepted_formats = ("jpg", "jpeg", "png")
folders = (
    "МА практика",
    "ДУ практика",
    "ДМиМЛ практика",
    "ВМА практика",
    "МА конспект",
    "ДУ конспект",
    "ДМиМЛ конспект",
    "ВМА конспект",
    "Другое")


class Button(Enum):
    SEND = 1
    FIND = 2
    NONE = 3


class User:
    user_id = 0
    first_name = ""
    subject_id = -1
    photos = []
    files = []
    button_state = Button(3)

    def __init__(self, user_id, first_name):
        self.user_id = user_id
        self.first_name = first_name
