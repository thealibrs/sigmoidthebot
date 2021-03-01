from telegram.ext import Updater
from bs4 import BeautifulSoup
from datetime import date
import constants, requests


# book command
def getBook(update, content):
    try:
        name = update.message.text.lower().split()
        requested_book = '%20'.join(name[1:])

        r = requests.get("https://tr.b-ok.as/s/"+requested_book)

        soup = BeautifulSoup(r.content, "lxml")

        tablo = soup.find('div', {'id': 'searchResultBox'})
        books = tablo.find_all('div', {'class': 'resItemBox resItemBoxBooks exactMatch'})

        message = str()
        for book in books[:5]:
            book_name = book.find('h3').text
            link = book.find('a').get('href')
            full_link = "https://tr.b-ok.as/"+link

            message += book_name+"\n"+full_link+"\n"
    
        update.message.reply_text(message)
    except:
        error_text = "Ama hangi kitap yahu!?🤔 \nKitap ararken '/kitapbul kitap adi' şeklinde ve kitap ismi belirtirken Türkçe karakter kullanmadığında beni çok mutlu edersin😉."

        update.message.reply_text(error_text)

# wheather command
def getWeather(update,content):
    try:
        city = update.message.text.split()[1].lower()

        r = requests.get("https://www.hurriyet.com.tr/hava-durumu/"+city+"/")
        soup = BeautifulSoup(r.content, "lxml")

        others = soup.find('div', {'class':'swiper-container'})
        others_date = others.find_all('div', {'class':'col-3 swiper-slide'})

        info=str()
        for od in others_date:
            date = od.find('div', {'class':'content-card-date'}).text
            cond = od.find('div', {'class':'content-card-condition'}).text
            temp = od.find('div', {'class':'content-card-temp'}).text

            info += date+"\n"+cond+"  "+temp+"\n\n"

        update.message.reply_text(info)
    except:
        error_text = "Ama hangi şehir? 🤔 \nHava durumunu merak ettiğinde '/havadurumu sehir' şeklinde ve şehir ismi belirtirken Türkçe karakter kullanmadığında beni çok mutlu edersin😉."

        update.message.reply_text(error_text)


# burc yorumu
def commentZodiac(update, content):
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")

    try:
        zodiac = update.message.text.split()[1].lower()
        r = requests.get("https://twitburc.com.tr/gunluk-burc-yorumlari/"+zodiac+".html")
        soup = BeautifulSoup(r.content, 'lxml')

        burc = soup.find('div', attrs={'class': 'thumbnail'})

        burc_baslik = burc.find('h2').text
        burc_icerik = burc.find('article').text[len(burc_baslik):]

        burc_yorum = """{}\n\n{}\n\n{}""".format(d1,burc_baslik, burc_icerik)

        update.message.reply_text(burc_yorum)
    except:
        error_text = "Peki hangi burç?!😯 \nBurcunu merak ettiğinde '/gunlukburc burcun' şeklinde yazmanı ve burç belirtirken Türkçe karakter kullanmamanı rica ediyorum🙂."

        update.message.reply_text(error_text)

# Kur verilerini çekmek için
def getCurrencies(update, content):
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")

    r = requests.get("https://kur.doviz.com")
    soup = BeautifulSoup(r.content, "lxml")
    currencies = soup.find_all('div', attrs={'class': 'item'})
    currency_text = str()

    for currency in currencies:
        currency1 = currency.find('a')
        currency_name = currency1.find('span', attrs={'class': 'name'}).text
        currency_value = currency1.find('span', attrs={'class': 'value'}).text

        currency_text += currency_name + " : " + currency_value+"\n"

    update.message.reply_text(d1+"\n"+currency_text)

# Haber verilerini çekmek için  
def getNews(update, content):
  r = requests.get("https://www.haberler.com/son-dakika/")
  soup = BeautifulSoup(r.content, "lxml")
  news = soup.find_all('div', attrs={'class':"hblnBox"})

# ilk 5 haberi döndürür
  for new in news[:5]:
    # haber linklerini aldık
    new_link = new.find("div", attrs={'class':'hblnContent'})
    link = new_link.a.get('href')

    # haber başlıklarını alalım
    title = new.find('a', attrs={'class':"hblnTitle"})
    new_title = title.get("title")

    # Saat bilgisini alalım
    time = new.find('div', attrs={'class':'hblnTime'}).text

    #uygun formatta yazdıralım
    haberler = """{}\n\n{}\n\n{}""".format(time, new_title, link)
    update.message.reply_text(haberler)

def help_command(update, context):
    message = constants.WELCOME_MESSAGE
    update.message.reply_text(message)

def wrongCommand(update, context):
    update.message.reply_text(constants.SORRY_MESSAGE)

def start_command(update, context):
    message = constants.START_MESSAGE
    update.message.reply_text(message)
