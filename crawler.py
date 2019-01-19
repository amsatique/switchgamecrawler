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

print "Bot ready to share happyness"
while True:
    curDate = datetime.now().strftime("%Y%m%d%H%M")
    html = urlopen('https://3ds-paradise.com/list.php?console=switch').read()
    soup = BeautifulSoup.BeautifulSoup(html, "html.parser")
    iso=soup.find('tbody')
    rows = iso.find_all('tr')
    for row in rows:
        data = extract(row)
        delta = int(curDate) - int(data[2])
        if int(delta) < int(delay):
            print data[0]
            bot.sendMessage(channel_id, data[0] + "-" + data[1] + "\n"+  data[3] + "\n")
    print "[" + curDate + "] Send ok"
    time.sleep( int(delay) * 60 )
