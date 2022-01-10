from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import requests
import json

bot = Bot(token="1727160002:AAF-jG2nzZJfWGXrXVcngLf9bFgt3I84t3c")

dp = Dispatcher(bot)