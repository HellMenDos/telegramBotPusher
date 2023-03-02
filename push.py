import os
import time
import json
import requests
from datetime import datetime
import asyncio
import aiohttp
import aiogram.utils.markdown as fmt
from aiogram import  types


TOKEN = "*****"

async def download(session,user,pushData):
    global TOKEN
    method = "sendMessage"
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    text = f'<b>{pushData["title"]}</b> \n\n{pushData["describe"]}'
    
    if pushData['photo']:
        photo = pushData["photo"].split('/').pop()
        urlPhoto = f'****{photo}'
        text = f'{fmt.hide_link(urlPhoto)}' + text

    data = {
        "chat_id": user,
        "text": text,
        'parse_mode': types.ParseMode.HTML
    }

    async with session.post(url, data=data) as response:
        await asyncio.sleep(1)
        return await response.json()

async def main(loop, pushData, users,pushName):
    async with aiohttp.ClientSession(loop=loop) as session:
        print('start')
        tasks=[asyncio.create_task(download(session, user, pushData)) for user in users]
        gatherTasks = await asyncio.gather(*tasks)

        if not os.path.isdir(f'send_datas/{pushName}'):
            os.mkdir(f'send_datas/{pushName}')

        with open(f'send_datas/{pushName}/{datetime.now()}data.json', 'w', encoding='utf-8') as f:
            json.dump(gatherTasks, f, ensure_ascii=False, indent=4)
            print('end')


if __name__=='__main__':
    domain = '******'
    data = requests.get(f'{domain}/user/all/').json()
    slicedData = [data[d:d+500] for d in range(0, len(data), 500)]
    pushName = input('Name of pushes: ') 
    pushId = input('pass push id: ') 
    data = requests.get(f'{domain}/push/one/{pushId}/').json()

    startTime = time.time()
    loop=asyncio.get_event_loop()
    for index, items in enumerate(slicedData):
        userTokens = [item['title'] for item in items]
        loop.run_until_complete(main(loop,data,userTokens,pushName))
        print('Sleep')
        time.sleep(10)

    print(time.time() - startTime)
