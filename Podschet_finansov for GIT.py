#!/usr/bin/env python
# coding: utf-8

# In[1]:


import telebot
from telebot import types
import requests

telebot.apihelper.SESSION = requests.Session()
telebot.apihelper.SESSION.timeout = 100

bot = telebot.TeleBot('xxxxxx') #Enter a code API


# In[2]:


import pandas as pd
df = pd.read_excel("budget.xlsx")
# df = pd.DataFrame(columns=['user', 'summa', 'prichina'])
# df


# In[ ]:


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global df
    
    Vik_sum = df[df.user == "Man1"].summa.sum()
    Lev_sum = df[df.user == "Man2"].summa.sum()
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Таблица")
    btn2 = types.KeyboardButton("Итоги")
    btn3 = types.KeyboardButton("Отменить последний")
    markup.add(btn1, btn2, btn3)
    
    if message.from_user.id == xxx or message.from_user.id == xxx: #Enter your TelegramID
        current_customer = "Man1"
    elif message.from_user.id == xxx: #Enter your TelegramID
        current_customer = "Man2"
    else:
        bot.send_message(message.from_user.id, "Вы не авторизованы для участия в чате")
        return 
    
    if message.text == "Таблица":
        bot.send_document(message.from_user.id, document=open('budget.xlsx', 'rb'))
        return
    if message.text == "Итоги":
        messaga = "Викусик: " + str(Vik_sum) + "    " + "Левик: " + str(Lev_sum) + "\nКаждому по: " + str((Vik_sum + Lev_sum)/2) + "\nЛевик отправляет Викусику: " + str(Lev_sum - (Vik_sum + Lev_sum)/2)
        bot.send_message(message.from_user.id, messaga)
        return
    if message.text == "Отменить последний":
        if df.empty:
            bot.send_message(message.from_user.id, "Список пуст, удаление невозможно")
            return
        else:
            index_to_remove = df.iloc[-1].name
            bot.send_message(message.from_user.id, "Удаляю " + str(df.loc[index_to_remove]["summa"]) + " " + str(df.loc[index_to_remove]["prichina"]))
            df = df.drop(index_to_remove)
            writer = pd.ExcelWriter('budget.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            writer.save()
            return
    
    text = message.text
    space_index = text.find(' ')
    
    if space_index != -1:
        number = text[:space_index]
        try:
            number = float(number)
        except ValueError:
            bot.send_message(message.from_user.id, "Сумма указана неверно", reply_markup=markup)
            return 
        text_part = text[space_index + 1:]
    else: 
        bot.send_message(message.from_user.id, "Причина не указана", reply_markup=markup)
        return 
    
    df = df.append({'user': current_customer, 'summa': number, 'prichina' : text_part}, ignore_index=True)
    
    bot.send_message(message.from_user.id, "Платеж внесён", reply_markup=markup)
    writer = pd.ExcelWriter('budget.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()
    
bot.polling(none_stop=True, interval=0)  # Обязательная для работы бота часть


# In[ ]:




