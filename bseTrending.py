import bs4
import requests


data = requests.get('https://www.moneycontrol.com/stocks/marketstats/bsemact1/index.php').text
soup = bs4.BeautifulSoup(data, features="html.parser")

allCompanies = soup.find_all('span', class_='gld13 disin')

allCompaniesList = []
for company in allCompanies:
    link = company.find('a').text
    allCompaniesList.append(link)

tableRow = soup.find_all('tr')

companyHigh = []
for tr in tableRow:
    high = tr.find_all('td', attrs={'width':175, 'align': 'right'})
    if len(high) == 0:
        continue
    for i in high:
        i = i.text.replace(',', '')
        companyHigh.append(float(i))
        break

print(companyHigh)