# -*- coding: utf-8 -*-

import os
import json
import logging
import configparser
from logging.handlers import TimedRotatingFileHandler
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    Updater, CommandHandler, CallbackContext, MessageHandler, 
    Filters , CallbackQueryHandler
)

import xui.api as api
import xui.utils as utils
from xui.users import Users

if not os.path.exists('logs'):
    os.makedirs('logs')

log_file_path = os.path.join('logs', 'xui.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S'
)

file_handler = TimedRotatingFileHandler(log_file_path, when='midnight', backupCount=30)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s'))
logger = logging.getLogger()
logger.addHandler(file_handler)

def load_configs():
    global TOKEN, admin_chatids, panel_username, \
        panel_password, panel_ip, panel_port, default_lang
    
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")

    TOKEN = cfg.get("telegram.bot", "token")
    admin_chatids = cfg.get("telegram.bot", "admin_chatids").split(",")
    panel_ip = cfg.get("xui-server", "ip")
    panel_port = cfg.get("xui-server", "port")
    panel_username = cfg.get("xui-server", "panel_username")
    panel_password = cfg.get("xui-server", "panel_password")
    default_lang = cfg.get("telegram.bot", "default_language")

    logger.info("Configs reloaded.")


with open("locals/messages.json", "r") as f:
    messages = json.loads(f.read())

load_configs()
xui = api.XUI(
    ip = panel_ip,
    port = panel_port,
    username = panel_username,
    password = panel_password
)
users = Users()


def start_command(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages[default_lang]["start"]
    )
    users.add_user(
        username=update.effective_user.username,
        chat_id=update.effective_user.id
    )

def help_command(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=messages[default_lang]["help"]
    )

def admin_panel_command(update: Update, context: CallbackContext):
    if not str(update.effective_chat.id) in admin_chatids:
        return
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="admin panel activated."
    )
    


def text_message(update: Update, context: CallbackContext):
    message = update.message
    context.bot.send_message(
        chat_id=message.chat_id,
        text=messages[default_lang]["unknown-text"]
    )




updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# ommand handlers
dispatcher.add_handler(CommandHandler('start', start_command))
dispatcher.add_handler(CommandHandler('help', help_command))
dispatcher.add_handler(CommandHandler('admin_panel', admin_panel_command))

# message handler
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), text_message))

# callback handler for inline keyboard



updater.start_polling()
updater.idle()