from datetime import datetime
import time
import schedule
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import scraping.py as scp

TOKEN = open('token.txt', 'r').read()