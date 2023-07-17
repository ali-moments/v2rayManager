from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardButton as IKB, InlineKeyboardMarkup as IKM, CallbackQuery


class before_login:
    def __init__(self):
        self.first_panel = {}
    
    def get_starter_keys(self):
        if self.first_panel:
            return self.first_panel
        kb = [[KeyboardButton("Show price"), KeyboardButton("How to connect")], [KeyboardButton("Log-in"), KeyboardButton("Sign-up")], [KeyboardButton("Connect to Support"), KeyboardButton("Rules and QA")], [KeyboardButton("Get Free Config!!")]]
        self.first_panel = ReplyKeyboardMarkup(kb, one_time_keyboard=True)
        return self.first_panel

class admin_panel:
    def __init__(self):
        self.first_panel = {}
    