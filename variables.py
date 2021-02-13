import telebot
from enum import Enum

bot = telebot.TeleBot('1165511829:AAHAp5NsBFMvbYzNjTzeU0Esl0nDS-XYBXY', threaded=False)
users = []
DEL = '/'
phrase1 = "Найти дз"
phrase2 = "Отправить тетрадку"
accepted_formats = ("jpg", "jpeg", "png")
folders = (
    "МА практика",
    "ДУ практика",
    "ТВиМС практика",
    "МЧА практика",
    "ФАиИУ практика",
    "ФАиИУ конспект",
    "ОСи конспект",
    "МА конспект",
    "ДУ конспект",
    "ТВиМС конспект",
    "МЧА конспект",
    "Физра",
    "Другое")


class Button(Enum):
    SEND = 1
    FIND = 2
    NONE = 3


class User:
    def __init__(self, message):
        self.user_id = message.from_user.id
        self.first_name = message.from_user.first_name
        self.last_name = message.from_user.last_name
        self.username = message.from_user.username
        self.subject_id = -1
        self.photos = []
        self.files = []
        self.button_state = Button(3)
