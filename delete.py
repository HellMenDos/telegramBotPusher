import os
from datetime import datetime
from os import listdir
import asyncio
from pydoc import describe
import aiohttp
import time
import aiogram.utils.markdown as fmt
from aiogram.types import ParseMode
from aiogram import Bot, Dispatcher, types
import json


TOKEN = "*****"

async def download(session, messageData):
    global TOKEN
    method = "deleteMessage"
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    if messageData['ok']:
        data = {
            "chat_id": messageData['result']['chat']['id'],
            "message_id": messageData['result']['message_id']
        }

        async with session.post(url, data=data) as response:
            return await response.json()

async def main(loop, fileName, folder):
    with open(fileName) as file:
        async with aiohttp.ClientSession(loop=loop) as session:
            tasks=[asyncio.create_task(download(session, messageData)) for messageData in json.load(file)]
            gatherTasks = await asyncio.gather(*tasks)

            if not os.path.isdir(f'delete_datas/{folder}'):
                os.mkdir(f'delete_datas/{folder}')

            with open(f'delete_datas/{folder}/{datetime.now()}data.json', 'w', encoding='utf-8') as f:
                json.dump(gatherTasks, f, ensure_ascii=False, indent=4)
                print('end')



if __name__=='__main__':
    folder = input('Pass folderName ')
    files = [f for f in listdir(f'send_datas/{folder}')]

    startTime = time.time()
    loop=asyncio.get_event_loop()
    for file in files:
        loop.run_until_complete(main(loop,f'send_datas/{folder}/{file}',folder))
        time.sleep(4)

    print(time.time() - startTime)


