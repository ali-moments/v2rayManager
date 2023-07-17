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


class show_price:
    def __init__(self):
        self.first_panel = {}

class how_to_connect:
    def __init__(self):
        self.first_panel = {}

class login:
    def __init__(self):
        self.first_panel = {}

class signup:
    def __init__(self):
        self.first_panel = {}

class support:
    def __init__(self):
        self.first_panel = {}

class rules_qa:
    def __init__(self):
        self.first_panel = {}

class free_config:
    def __init__(self):
        self.first_panel = {}

class cancel:
    def __init__(self):
        self.first_panel = {}

    def get_starter_keys(self):
        if self.first_panel:
            return self.first_panel
        kb = [[KeyboardButton("Cancel")]]
        self.first_panel = ReplyKeyboardMarkup(kb, one_time_keyboard=True)
        return self.first_panel