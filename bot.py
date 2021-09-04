import logging
import settings
from telegram.ext import Updater
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(filename='bot.log', level=logging.INFO)

def greet_user(update, context):
    print("Вызвана команда /start")
    update.message.reply_text("Привет! Ты вызвал команду /start")

def main():
    mybot = Updater(settings.TOKEN, use_context = True)
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
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