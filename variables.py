import telebot
from enum import Enum

bot = telebot.TeleBot('972251801:AAEC8f-WjE1QG1s-36y2Jgk0zniwrbv5KLE', threaded=False)
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
    last_name = ""
    username = ""
    subject_id = -1
    photos = []
    files = []
    button_state = Button(3)

    def __init__(self, message):
        self.user_id = message.from_user.id
        self.first_name = message.from_user.first_name
        self.last_name = message.from_user.last_name
        self.username = message.from_user.username
