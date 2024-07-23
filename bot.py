#!/usr/bin/env python
# coding: utf-8

# In[1]:


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
        
        formatted_results = []
        for panel_default in panel_defaults:
            panel_body = panel_default.find("div", class_="panel-body")
            if panel_body:
                strong_tag = panel_body.find("strong")
                if strong_tag:
                    term = strong_tag.text.strip().replace("Bahasa indonesia-nya kata: ", "")
                    meaning = panel_body.find("i").text.strip() if panel_body.find("i") else ""
                    formatted_results.append(f"{term}\n ⮕{meaning}")
        
        return "\n".join(formatted_results)
    
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def get_meaning(word):
    url = f"https://kata.web.id/kamus/jawa-indonesia/cari/{word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    word_entries = soup.find_all("a", class_="bg-white dark:bg-gray-600 p-6 rounded-lg border border-gray-200 shadow-md hover:bg-gray-100 dark:border-gray-600 dark:hover:bg-gray-800")
    meanings = []
    for entry in word_entries:
        entry_word = entry.find("h5").text
        entry_meaning = entry.find("p").text
        meanings.append(f"{entry_word}\n⮕{entry_meaning}")

    return "\n".join(meanings) if meanings else f"找不到單詞 {word} 的意思。"

def handle_message(update, context):
    user_input = update.message.text
    # Get results from the first website
    result1 = search_kamusjawa(user_input)
    
    # Get results from the second website
    result2 = get_meaning(user_input)
    
    if result1:
        update.message.reply_text(f"第一個網站的結果：\n{result1}\n第二個網站的結果：\n{result2}")
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


# In[ ]:




