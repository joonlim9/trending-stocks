import bs4
import requests


data = requests.get('https://www.moneycontrol.com/stocks/marketstats/bsemact1/index.php').text
soup = bs4.BeautifulSoup(data, features="html.parser")

allCompanies = soup.find_all('span', class_='gld13 disin')

# company list
companiesList = []
for company in allCompanies:
    link = company.find('a').text
    companiesList.append(link)


tableRow = soup.find_all('tr')
companyLow = []
companyClose = []
companyHigh = []
companyChange = []
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
    low = tr.find_all('td', attrs={'width': 180, 'align': 'right'})
    for i in low:
        i = i.text.replace(',', '')
        companyLow.append(float(i))

    # close price (last price)
    close = tr.find_all('td', attrs={'width':185, 'align': 'right'})
    for i in close:
        i = i.text.replace(',', '')
        companyClose.append(float(i))

    # change of price
    change = tr.find_all('td', attrs={'width': 175, 'align': 'right'})
    for i in change:
        if i.has_attr('class'):
            companyChange.append(float(i.text))


companyData = []

for i in range(len(companiesList)):
    companyData.append({
        'company': companiesList[i],
        'high_price': companyHigh[i],
        'low_price': companyLow[i],
        'change_percentage': companyChange[i],
        'close_price': companyClose[i]
    })

print(companyData)