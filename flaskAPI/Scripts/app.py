from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return '<h1>Hello World!!<h1/>'


@app.route("/trending", methods=['GET'])
def trending():
    data = requests.get(
        'https://www.moneycontrol.com/stocks/marketstats/bsemact1/index.php').text

    soup = BeautifulSoup(data, 'lxml')

    allCompanies = soup.find_all('span', class_='gld13 disin')

    companiesList = []
    for row in allCompanies:
        link = row.find('a').text
        companiesList.append(link)

    tablerow = soup.find_all('tr')

    companyHigh = []
    companyLow = []
    companyClose = []
    companyChange = []
    for tr in tablerow:
        # high price
        high = tr.find_all('td', attrs={'width': 175, 'align': 'right'})
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

        # close price
        close = tr.find_all('td', attrs={'width': 185, 'align': 'right'})

        for i in close:
            i = i.text.replace(',', '')
            companyClose.append(i)

        # change in price
        change = tr.find_all('td', attrs={'width': 175, 'align': 'right'})

        for i in change:
            if i.has_attr('class'):
                companyChange.append(float(i.text))

    companyData = []

    for i in range(len(companiesList)):
        companyData.append({
            'company': companiesList[i],
            'high': companyHigh[i],
            'low': companyLow[i],
            'change_in_per': companyChange[i],
            'close': companyClose[i]
        })

    new_dict = sorted(

        companyData, key=lambda i: i['change_in_per'], reverse=True
    )

    return jsonify(data=(new_dict)), 201


@app.route("/gainers", methods=['GET'])
def gainers():
    data = requests.get(
        'https://www.moneycontrol.com/stocks/marketstats/bsegainer/index.php').text

    soup = BeautifulSoup(data, 'lxml')

    # company names

    allCompanies = soup.find_all('span', class_='gld13 disin')

    companiesList = []

    for i in allCompanies:
        a = i.find('a')
        companiesList.append(a.text)

    tablerow = soup.find_all('tr')
    companyHigh = []
    companyLow = []
    companyClose = []
    companyGain = []
    companyChange = []

    for tr in tablerow:
        # high price
        high = tr.find_all('td', attrs={'width': 75, 'align': 'right'})

        for i in high:
            i = i.text.replace(',', '')
            companyHigh.append(float(i))

        # low price

        low = tr.find_all('td', attrs={'width': 80, 'align': 'right'})

        for i in low:
            i = i.text.replace(',', '')
            companyLow.append(float(i))
            break

        # close or last price
        close = tr.find_all('td', attrs={'width': 85, 'align': 'right'})

        for i in close:
            i = i.text.replace(',', '')
            companyClose.append(float(i))
            break

        # gain
        gain = tr.find_all(
            'td', attrs={'width': 45, 'align': 'right', 'class': 'green'})
        if len(gain) == 0:
            continue
        companyGain.append(float(gain[0].text))

        # change in price
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

    return jsonify(data=(companyData)), 201


@app.route("/losers", methods=['GET'])
def losers():
    data = requests.get(
        'https://www.moneycontrol.com/stocks/marketstats/bseloser/index.php').text
    soup = BeautifulSoup(data, 'lxml')

    allCompanies = soup.find_all('span', class_='gld13 disin')

    companiesList = []
    for row in allCompanies:
        alink = row.find('a')
        companiesList.append(alink.text)

    tablerow = soup.find_all('tr')

    companyHigh = []
    companyLow = []
    companyClose = []
    companyChange = []
    companyLoss = []

    for tr in tablerow:
        high = tr.find_all('td', attrs={'width': 75, 'align': 'right'})

        for i in high:
            chigh = i.text.replace(',', '')
            companyHigh.append(chigh)
            break

        low = tr.find_all('td', attrs={'width': 80, 'align': 'right'})

        for i in low:
            clow = i.text.replace(',', '')
            companyLow.append(clow)
            break

        close = tr.find_all(
            'td', attrs={'width': 85, 'align': 'right'})

        for i in close:
            cclose = i.text.replace(',', '')
            companyClose.append(cclose)
            break

        change = tr.find_all(
            'td', attrs={'width': 45, 'align': 'right', "class": 'red'})
        if len(change) == 0:
            continue
        for i in change:

            cchange = i.text.replace(',', '')
            companyChange.append(cchange)
            break

        loss = tr.find_all(
            'td', attrs={'width': 45, 'align': 'right', "class": 'red'})
        if len(loss) == 0:
            continue

        companyLoss.append(float(loss[1].text.replace(',', '')))

    companyData = []

    for i in range(len(companiesList)):
        companyData.append({
            'company': companiesList[i],
            'High': float(companyHigh[i]),
            'Low': float(companyLow[i]),
            'Change': float(companyChange[i]),
            'Loss_in_per': float(companyLoss[i]),
            'close_price': float(companyClose[i])
        })

    new_dict = sorted(companyData, key=lambda i: i['Loss_in_per'])

    return jsonify(data=(new_dict)), 201


if __name__ == '__main__':
    app.run(debug=True)
