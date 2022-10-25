from requests_html import HTMLSession
from bs4 import BeautifulSoup

import mysql.connector

def getNumber(line):
    txt = str(line)
    items = txt.split(",")
    items2 = []
    items3 = []
    out = ''
    for item in items:
        a = item.split("<")
        for b in a:
            items2.append(b)
    for item in items2:
        c = item.split(">")
        for d in c:
            items3.append(d)
    for item in items3:
        char = item[:1]
        if char.isdigit() or char == '-':
            out = item
    return out


cnx=mysql.connector.connect(
    user = 'jlclark',
    password ='givememydata',
    host ='jlclark.mysql.pythonanywhere-services.com',
    database ='jlclark$stocks'
)

cursor = cnx.cursor()

session = HTMLSession()
page = session.get('https://finance.yahoo.com/u/yahoo-finance/watchlists/most-added')

soup = BeautifulSoup(page.content,"html.parser")
tables = soup.find_all('table')
stocks = tables[1].tbody
#for table in tables:
 #   print(type(table))
rows = stocks.find_all('tr')
n = 0

for row in rows:
    infos = row.find_all('td')
    symbol = str(infos[0].string)
    name = str(infos[1].string)
    price = str(infos[2].string)
    sect = str(infos[3].span)
    chng = getNumber(sect)
    sql = "INSERT INTO watchlist (symbol, name, lastPrice, deltaPrice, time) VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP())"
    val = (symbol, name, price, chng)
    cursor.execute(sql,val)
    n = n + cursor.rowcount

print(n, " rows added")

cnx.commit()
cnx.close()





