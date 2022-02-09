import json
import requests
TOKEN = '5252793321:AAG3wJoRVlXo-SJ12trF-edZ3VIENPpIFjI'
chat_id = '732897762'
text = ''

imp = requests.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')

json_rates = json.loads(imp.text)
currency = 'USD'
for i in json_rates:
    if currency == i['ccy']:
        text = f'Курс долара: \n {i["ccy"]} \n {i["buy"]} \n {i["sale"]}'
    elif currency == i['ccy']:
        text = f'Курс євро: \n {i["ccy"]} \n {i["buy"]} \n {i["sale"]}'
    elif currency == i['ccy']:
        text = f'Курс російського рубля: \n {i["ccy"]} \n {i["buy"]} \n {i["sale"]}'
        print(text)
    try:
        sting = int(input("Введіть назву валюти: "))
        print()
    except:
        print("Невдала спроба")


telegram_url = f'https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}'

telegram_request = requests.get(telegram_url)

