import os
import requests
import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# 🔹 你的 Telegram Bot API Token
TELEGRAM_BOT_TOKEN = "你的API_TOKEN"  # ⚠️ 替换成你的真实 Token

# 🔹 API 地址（获取主播列表）
ONLINE_USERS_API = "https://lese8u.dcdhcms.xyz//appapi/?service=Home.getHot&uid=12641007&p=1&token=ba6d1e3ce9021d3e228380943a425312&oaid="
LIVE_STREAM_API = "https://9arpa2j0.ewsions.xyz/appapi/?service=Live.getLiveInfo&liveuid={}"

# 生成 M3U 播放列表
def generate_m3u():
    try:
        response = requests.get(ONLINE_USERS_API, timeout=10)
        response.raise_for_status()
        data = response.json()

        # 获取在线主播 UID
        uids = [(user["uid"], user["user_nickname"]) for user in data["data"]["info"][0]["list"]]
        if not uids:
            return None

        m3u_file = "kuyou_live.m3u"
        with open(m3u_file, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for uid, nickname in uids:
                stream_url = get_live_stream(uid)
                if stream_url:
                    f.write(f"#EXTINF:-1,{nickname}\n{stream_url}\n")

        return m3u_file
    except Exception as e:
        print(f"❌ 生成直播源失败: {e}")
        return None

# 获取单个主播的直播流
def get_live_stream(uid):
    try:
        url = LIVE_STREAM_API.format(uid)
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "data" in data and "info" in data["data"] and data["data"]["info"]:
            return data["data"]["info"][0].get("pull", "")
    except Exception as e:
        print(f"❌ 获取 UID {uid} 直播源失败: {e}")
    return None

# 处理 Telegram `/m3u` 命令
def send_m3u(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    bot = context.bot

    update.message.reply_text("📡 生成直播源中，请稍等...")
    m3u_file = generate_m3u()

    if not m3u_file:
        update.message.reply_text("❌ 没有找到在线直播源！")
        return

    # 发送 M3U 文件
    bot.send_document(chat_id=chat_id, document=open(m3u_file, "rb"), caption="🎬 你的直播源文件已生成！")

# 启动 Telegram Bot
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("m3u", send_m3u))

    print("🚀 机器人已启动！发送 /m3u 生成直播源")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
