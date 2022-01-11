import bs4
import requests
import pprint

def bseTrending():
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
    companyGain = []
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

        # gain
        gain = tr.find_all(
            'td', attrs={'width': 45, 'align': 'right', 'class': 'green'})
        if len(gain) == 0:
            continue
        companyGain.append(float(gain[0].text))

        # change
        change = tr.find_all(
            'td', attrs={'width': 55, 'align': 'right', 'class': 'green'})
        if len(change) == 0:
            continue
        companyChange.append(float(change[0].text))

    companyData = []

    for i in range(len(companiesList)):
        companyData.append({
            'company': companiesList[i],
            'high': companyHigh[i],
            'low': companyLow[i],
            'change': companyChange[i],
            'gain_in_per': companyGain[i],
            'close_in_per': companyClose[i]
        })

    for i in range(len(companiesList)):
        pprint.pprint(companyData[i])
        print(' ')

bseTrending()