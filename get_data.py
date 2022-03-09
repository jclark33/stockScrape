from requests_html import HTMLSession
from bs4 import BeautifulSoup

session = HTMLSession()
page = session.get('https://finance.yahoo.com/u/yahoo-finance/watchlists/most-added')

soup = BeautifulSoup(page.content,"html.parser")
tables = soup.find_all('tbody')
#for table in tables:
 #   print(type(table))
stocks = tables[1]
rows = stocks.find_all('tr')
for row in rows:
    infos = row.find_all('td')
    for info in infos:
        print(info.text)