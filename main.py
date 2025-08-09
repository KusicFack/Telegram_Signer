from config import api_id, api_hash
from telethon import TelegramClient
import asyncio, os, datetime

log_file = open(os.path.join(os.path.dirname(__file__), "log.txt"),'a',encoding="UTF-8")

def dual_print(text):
    print(text)
    log_file.write(text+'\n')

# KusicFack 处替换自定义名字，第一次使用脚本时需要经历完整的登录流程，然后会在脚本目录下生成“自定义名字.session”文件来保存登录凭证
client = TelegramClient("KusicFack",api_id=api_id, api_hash=api_hash, proxy=("SOCKS5","127.0.0.1",7897))

async def main():
    dual_print(("脚本执行时间："+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")).center(os.get_terminal_size().columns-7,"="))
    try:
        user = await client.get_me()
        dual_print(f"已登录：{user.first_name}{user.last_name}，准备签到...")

        # 记录当前最新消息
        last_message = await anext(client.iter_messages("@ure_best_bot", limit=1))

        # 开始签到
        dual_print("开始签到...")
        await client.send_message("@ure_best_bot","/checkin")

        # 等待签到结果
        dual_print("等待签到结果...")
        for _ in range(5):
            await asyncio.sleep(0.5)
            new_message = await anext(client.iter_messages("@ure_best_bot", limit=1))
            if new_message.id > last_message.id:
                dual_print("签到结果："+ new_message.text)
                break
            if _ == 4: raise Exception("未收到签到结果回复！")
    except Exception as e:
        dual_print("签到失败！错误信息："+str(e))
    dual_print("")

with client:
    client.loop.run_until_complete(main())