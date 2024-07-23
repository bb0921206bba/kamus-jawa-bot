#!/usr/bin/env python
# coding: utf-8

# In[9]:


import urllib3
import requests
from bs4 import BeautifulSoup
import telegram
from telegram.ext import Updater, MessageHandler, Filters

def search_kamusjawa(word):
    base_url = "https://www.kamusjawa.net/kamus"
    params = {"teks": word, "bahasa": "bahasa", "submit": "LIHAT HASIL TERJEMAHAN"}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        panel_defaults = soup.find_all("div", class_="panel panel-default")
        
        meanings = []
        for panel_default in panel_defaults:
            panel_body = panel_default.find("div", class_="panel-body")
            if panel_body:
                meaning = panel_body.text.strip()
                meanings.append(meaning)
        
        if meanings:
            return "\n\n".join(meanings)  # Separate meanings with double newline
        else:
            return "未找到該單字的意思。"
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def handle_message(update, context):
    user_input = update.message.text
    result = search_kamusjawa(user_input)
    if result:
        update.message.reply_text(f"單字「{user_input}」的意思是：\n\n{result}")
    else:
        update.message.reply_text("未找到該單字的意思。")

def main():
    # 使用你的機器人令牌初始化機器人
    bot_token = "6999288835:AAE91xgE2Jz3vbb2wmt7YjyzbNCcaJSCvkI"
    bot = telegram.Bot(token=bot_token)
    updater = Updater(bot=bot, use_context=True)
    dispatcher = updater.dispatcher

    # 設置處理用戶輸入的方法
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    # 開始接收用戶的訊息
    updater.start_polling()

    # 讓機器人一直運行，直到你手動停止
    updater.idle()

if __name__ == "__main__":
    main()

