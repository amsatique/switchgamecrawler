#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib2 import urlopen
from datetime import datetime
import bs4 as BeautifulSoup
import re
import os
import time
import telepot

## Check env var ##
if "TELEGRAM_CHANNEL_ID" not in os.environ:
    print("TELEGRAM_CHANNEL_ID needed, please come back with it !")
else:
    channel_id = os.environ['TELEGRAM_CHANNEL_ID']

if "TELEGRAM_TOKEN" not in os.environ:
    print("TELEGRAM_TOKEN needed, please come back with it !")
else:
    telegram_token = os.environ['TELEGRAM_TOKEN']

if "DELAY" not in os.environ:
    print("DELAY (in minutes) needed, please come back with it !")
else:
    delay = os.environ['DELAY']

cdn_url = "https://cdn01.nintendo-europe.com/media/images/11_square_images/games_18/nintendo_switch_download_software/SQ_NSwitchDS_"
bot = telepot.Bot(telegram_token)

def extract(row):
    td = row.find_all('td')
    link =  td[0].find('a')['href']
    start = str(td[0]).find('_blank">') + 8
    end = str(td[0]).find('</a></td>')
    name = str(td[0])[start:end]
    region = td[1].get_text()
    date = td[2].get_text()
    date = datetime.strptime(date , ' %Y/%m/%d %H:%M')
    date = date.strftime("%Y%m%d%H%M")
    return name, region, date, link

def get_img(name):
    slug = ""
    regexp = r'[-A-Za-z0-9]+'
    list = re.findall(regexp, name)
    for i in list:
        upper = i.capitalize()
        slug += upper
    url = cdn_url + slug + "_image500w.jpg"
    return url

print "[READY] Bot ready to share happiness"
while True:
    curDate = int(datetime.now().strftime("%Y%m%d%H%M")) + 100
    html = urlopen('https://3ds-paradise.com/list.php?console=switch').read()
    soup = BeautifulSoup.BeautifulSoup(html, "html.parser")
    iso=soup.find('tbody')
    rows = iso.find_all('tr')
    for row in rows:
        data = extract(row)
        delta = int(curDate) - int(data[2])
        if int(delta) < int(delay) and  int(delta) >= 0:
            url = get_img(data[0])
            bot.sendMessage(channel_id, data[0] + "-" + data[1] + "\n"+  data[3] + "\n")
            try:
                bot.sendPhoto(channel_id, url)
            except:
                print "Cannot find img"
    print "[ " + str(curDate) + " ] Send ok"
    print "Waiting for : " + str(int(delay) * 60 ) + " seconds"
    time.sleep( int(delay) * 60 )
