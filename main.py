from config import api_id, api_hash
from telethon import TelegramClient
import asyncio, os

log_file = open(os.path.join(os.path.dirname(__file__), "log.txt"),'a',encoding="UTF-8")

def dual_print(text):
    print(text)
    log_file.write(text+'\n')

client = TelegramClient("KusicFack",api_id=api_id, api_hash=api_hash, proxy=("SOCKS5","127.0.0.1",7897))

async def main():
    try:
        user = await client.get_me()
        dual_print(f"已登录：{user.name}，准备签到...")

        # 记录当前最新消息
        last_message = await anext(client.iter_messages(from_user="@ure_best_bot", limit=1))

        # 开始签到
        dual_print("开始签到...")
        await client.send_message("@ure_best_bot","/checkin")

        # 等待签到结果
        dual_print("等待签到结果...")
        for _ in range(5):
            await asyncio.sleep(0.5)
            new_message = await anext(client.iter_messages("@ure_best_bot", limit=1))
            if new_message.id > last_message.id:
                dual_print("签到结果：", new_message)
                break
            if _ == 4: raise Exception("未收到签到结果回复！")
    except Exception as e:
        dual_print("签到失败！错误信息："+str(e))

with client:
    client.loop.run_until_complete(main())