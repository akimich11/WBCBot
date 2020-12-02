import telebot

bot = telebot.TeleBot('972251801:AAEC8f-WjE1QG1s-36y2Jgk0zniwrbv5KLE', threaded=False)
ids = []
photos = []
phrase1 = "Скатать дз"
phrase2 = "Скинуть тетрадку"
user = ""
user_id = ""
last = ""
saved_index = -1
FolderNames = [
    "МА практика",
    "ДУ практика",
    "ДМиМЛ практика",
    "ВМА практика",
    "МА конспект",
    "ДУ конспект",
    "ДМиМЛ конспект",
    "ВМА конспект",
    "Другое"]


class UserAnd12:
    def __init__(self, u_id):
        self.u_id = u_id
        self.one_or_two = 0
