# -*- coding: utf-8 -*-

import configparser
from colorama import Fore
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import xui.api as api
from telegram.ext import CommandHandler, Updater



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
        panel_password, panel_ip, panel_port
    cfg = configparser.ConfigParser()
    cfg.read("config.ini")
    TOKEN = cfg.get("telegram.bot", "token")
    admin_chatids = cfg.get("telegram.bot", "admin_chatids").split(",")
    panel_ip = cfg.get("xui-server", "ip")
    panel_port = cfg.get("xui-server", "port")
    panel_username = cfg.get("xui-server", "panel_username")
    panel_password = cfg.get("xui-server", "panel_password")

    logger.info("Configs reloaded.")


load_configs()

xui = api.XUI(
    ip = panel_ip,
    port = panel_port,
    username = panel_username,
    password = panel_password
)

print(xui.get_clients(2))
