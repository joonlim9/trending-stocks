import bs4
import requests


data = requests.get('https://www.moneycontrol.com/stocks/marketstats/bsemact1/index.php').text
soup = bs4.BeautifulSoup(data, features="html.parser")

allCompanies = soup.find_all('span', class_='gld13 disin')

# company list
allCompaniesList = []
for company in allCompanies:
    link = company.find('a').text
    allCompaniesList.append(link)


tableRow = soup.find_all('tr')
companyLow = []
companyClose = []
companyHigh = []

for tr in tableRow:
    # high price
    high = tr.find_all('td', attrs={'width':175, 'align': 'right'})
    if len(high) == 0:
        continue
    for i in high:
        i = i.text.replace(',', '')
        companyHigh.append(float(i))
        break

    # low price
    low = tr.find_all('td', attrs={'widht': 180, 'align': 'right'})
    for i in low:
        i = i.text.replace(',', '')
        companyLow.append(float(i))

    # close price (last price)
    close = tr.find_all('td', attrs={'width':185, 'align': 'right'})
    for i in close:
        i = i.text.replace(',', '')
        companyClose.append(float(i))
    