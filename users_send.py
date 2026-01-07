import json
import os
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

api_id = int(os.getenv('API_ID'))  #! Преобразуем в число
api_hash = os.getenv('API_HASH')
session = os.getenv('SESSION')
password = os.getenv('PASSWORD')
phone = os.getenv('PHONE')

with open('messages.json', 'r', encoding='utf-8') as file:
    data = json.load(file)  # data - это массив объектов
user_ids = [item["user_id"] for item in data]
print(f"""ID пользователей из файла messages.json: {user_ids}""")

client = TelegramClient('session', api_id, api_hash)
client.send_message(user_ids[3], "Привет хочу работать у вас ремонтником")#! Цифру ставишь ту, текст которой понравился.
                               #!^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Любое другое сообщение