from telethon import TelegramClient
import asyncio
import os
from dotenv import load_dotenv
import json
from datetime import datetime
from secrets import randbelow

load_dotenv()

api_id = int(os.getenv('API_ID'))  #! Преобразуем в число
api_hash = os.getenv('API_HASH')
session = os.getenv('SESSION')
password = os.getenv('PASSWORD')
phone = os.getenv('PHONE')

async def main(search_by:str, limit_send_msgs:int):

    #! Создаем клиент с файловой сессией
    client = TelegramClient('session', api_id, api_hash)
    
    #! Авторизуемся
    await client.start(phone=phone, password=password)
    
    #! Проверяем авторизацию
    me = await client.get_me()
    print(f"✅ Авторизован как: {me.first_name} (@{me.username})")
    
    # Отправляем сообщение в Избранное
    # message_auth = await client.send_message('me', 'Зросвуйте')
    # print(f"✅ Сообщение отправлено! ID: {message_auth.id}")
    
    msgs = await client.get_messages("@Oleg_pro_killer", limit=limit_send_msgs)#! вставляешь свой айди аккаунта с которого будешь брать сообщения для рассылки
    
    result_parser = []#! массив с результатами(айди, сообщение, дата)
    seen_ids = set()
    i = 0
    while True:
        async for chat in client.iter_dialogs(archived=True):#! цикл. проходимся по ВСЕМ чатам на аккаунте, НО только из папки "Архив"
            
            result = await client.get_messages(chat, limit = 1000, search = search_by)#! Получаем последние 100 сообщений из чата с ключевым словом

            #!РАСКОММЕНТИРУЙ ЧТОБЫ РАССЫЛАТЬ:
            #! msg_id = randbelow(limit_send_msgs)

            #! await client.send_message(chat, msgs[msg_id])

            for message in result:#! для каждого подходящего сообщения

                # print("=======================")
                # print(id)
                # print(text_msg)

                date = message.date#! дата сообщения

                readable_date = date.strftime('%A, %d %B %Y, %H:%M')#! крутая дата сообщения

                id = message.sender.id#! айди пользователя выложившего сообщение(позднее будем их вытаскивать и отправлять приватные сообщ)

                text_msg = message.text#! текст сообщения
            
                if id not in seen_ids:
                    seen_ids.add(id) #! если айди пользователя ещё не было(от него еще не было сообщений)
                    result_parser.append({ #! Добавляем в результат
                        "counter": i,
                        "user_id": id,
                        "message": text_msg,
                        "time": readable_date
                    }) 
                    i+=1

                    
            print( f"""Отправлено в {chat.name}, время: {datetime.now()}""")#! Логгируем в терминал что рассылка на 1 чат завершена  
            #! РАСКОММЕНТИРУЙ ЕСЛИ ХОЧЕШЬ РАССЫЛАТЬ:   
            #! asyncio.sleep(5)    

        with open('messages.json', 'w', encoding='utf-8') as file:#! Сохраняем в 'messages.json'
            json.dump(result_parser, file, ensure_ascii=False, indent=2)
    
        print("✅ Файл messages.json создан!")
        print(f"""✅ Рассылка завершена, время: {datetime.now()}""")#! Логгируем что цикл закончился

        result_parser=[]
        await asyncio.sleep(3600) 

# Запускаем асинхронно
asyncio.run(main("ремонтник", 5))