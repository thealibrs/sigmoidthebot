from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bs4 import BeautifulSoup
import functions as f
import constants, requests

print("Bot Starting...")

def main():
    updater = Updater(constants.TOKEN, use_context=True)
    dp = updater.dispatcher

    #ana komutlar
    dp.add_handler(CommandHandler("start", f.start_command))
    dp.add_handler(CommandHandler("yardim", f.help_command))
    dp.add_handler(CommandHandler("kitapbul", f.getBook))
    dp.add_handler(CommandHandler("sondakika", f.getNews))
    dp.add_handler(CommandHandler("kurlar", f.getCurrencies))
    dp.add_handler(CommandHandler("gunlukburc", f.commentZodiac))
    dp.add_handler(CommandHandler("havadurumu", f.getWeather))

    #hatalı komut girilme durumunda
    dp.add_handler(MessageHandler(Filters.text, f.wrongCommand))

    updater.start_polling(1.5)
    updater.idle()

if __name__ == "__main__":
    main()
