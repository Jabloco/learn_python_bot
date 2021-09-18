import datetime
import logging
import settings
import ephem
import csv
from datetime import date, datetime
from telegram.ext import Updater
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(filename='bot.log', level=logging.INFO)

cities_list = []

with open("city.csv", "r") as cities:
    fields = ["city_id", "country_id", "region_id", "name"]
    reader = csv.DictReader(cities, fields, delimiter = ";")
    for row in reader:
        cities_list.append(row["name"].lower())

def calc(update, context):
    update.message.reply_text("Подсказка: '$' - целочисленное деление, '^' - возведение в степень ")
    primer = update.message.text
    primer_str = ''
    primer_list = []
    operators_list = []
    primer = primer.replace("/calc", "")#Убрал calc ("/" определяло как делить)
    
    #Делаем список из значений и операторов
    for i in primer:
        if i.isdigit() or i == ".":
            primer_str += i
        else:
            primer_str += " "
        primer_list = list(map(float, primer_str.split()))    
        if i =="*" or i =="/" or i =="$" or i =="^" or i =="%" or i =="+" or i =="-":
            operators_list.append(i)
    
    #Сначала считаем умножение, деление и т.д.
    for op in operators_list: 
        try:
            op_index = operators_list.index(op)
            while "*" in operators_list or "/" in operators_list or "$" in operators_list or "^" in operators_list or "%" in operators_list:
                if operators_list[op_index] == "*":
                    operators_list.pop(op_index)
                    number = primer_list.pop(op_index) * primer_list.pop(op_index)
                    primer_list.insert(op_index, number)    
                elif operators_list[op_index] == "$":
                    try:
                        operators_list.pop(op_index)
                        number = primer_list.pop(op_index) // primer_list.pop(op_index)
                        primer_list.insert(op_index, number)
                    except(ZeroDivisionError):
                        update.message.reply_text("Делишь на ноль!") 
                elif operators_list[op_index] == "/":
                    try:
                        operators_list.pop(op_index)
                        number = primer_list.pop(op_index) / primer_list.pop(op_index)
                        primer_list.insert(op_index, number)
                    except(ZeroDivisionError):
                        update.message.reply_text("Делишь на ноль!") 
                elif operators_list[op_index] == "^":
                    operators_list.pop(op_index)
                    number = primer_list.pop(op_index) ** primer_list.pop(op_index)
                    primer_list.insert(op_index, number)
                elif operators_list[op_index] == "%":
                    operators_list.pop(op_index)
                    number = primer_list.pop(op_index) % primer_list.pop(op_index)
                    primer_list.insert(op_index, number)           
                else:
                    break
        except(IndexError):
            update.message.reply_text("Внимание! Лишний знак!")            
    
    #Считаем сложение и вычитание
    for op in operators_list: 
        try:
            op_index = operators_list.index(op)
            if op == "+":
                number = primer_list.pop(0) + primer_list.pop(0)
                primer_list.insert(0, number)   
            if op == "-":
                number = primer_list.pop(0) - primer_list.pop(0)
                primer_list.insert(0, number)     
            else:
                continue
        except(IndexError):
            update.message.reply_text("Внимание! Лишний знак!")
               
    update.message.reply_text(number)

def city_game(update, context):
    city = update.message.text.split()[1].lower()
    while city in cities_list:
        for old_city in cities_list:
            if old_city[0].lower() == city[-1]:
                new_city = old_city
                cities_list.remove(old_city)
                cities_list.remove(city)
                break
        update.message.reply_text(f"{new_city.capitalize()} - твой ход!")
        break

    else:
        update.message.reply_text("Такого города нет!!!")

def greet_user(update, context):
    print("Вызвана команда /start")
    update.message.reply_text("Привет! Ты вызвал команду /start")

def next_full_moon(update, context):
    print("Вызвана команда /moon")
    
    full_moon_date = ephem.next_full_moon(date.today())
    update.message.reply_text(full_moon_date)

def sozvezdie(update, context):
    try:
        planet = update.message.text.split()[1].capitalize()
        m = getattr(ephem, planet)(date.today()) #потребовался атрибут объекта, а не строка
        constell = ephem.constellation(m) #чтобы не указывать сокращение созвездия
        update.message.reply_text(f"Планета {planet} в созвездии {constell[1]}.")
    except(AttributeError):
        update.message.reply_text("Такой планеты нет(")

def main():
    mybot = Updater(settings.TOKEN, use_context = True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("moon", next_full_moon))
    dp.add_handler(CommandHandler("planet", sozvezdie))
    dp.add_handler(CommandHandler("city", city_game))
    dp.add_handler(CommandHandler("calc", calc))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)

if __name__ == "__main__":
    main()