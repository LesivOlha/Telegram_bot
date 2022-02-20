import json
import requests


class TelegramBot:
    def __init__(self, chat_id, token):
        self.chat_id = chat_id
        self.token = token

    def get_json(self, url):
        data = requests.get(url)
        json_data = json.loads(data.text)
        return json_data

    def send_message(self, currency, from_id):
        json_rates = self.get_json('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
        text = ''
        for i in json_rates:
            if currency == 'USD' and i['ccy'] == 'USD':
                text = f'Курс долара: \n {i["ccy"]} \n {i["buy"]} \n {i["sale"]}'
                break
            elif currency == 'EUR' and i['ccy'] == 'EUR':
                text = f'Курс євро: \n {i["ccy"]} \n {i["buy"]} \n {i["sale"]}'
                break
            elif currency == 'RUR' and i['ccy'] == 'RUR':
                text = f'Курс російського рубля: \n {i["ccy"]} \n {i["buy"]} \n {i["sale"]}'
                break
        telegram_url = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={from_id}&text={text}'
        self.get_json(telegram_url)

    def first_message(self, from_id):
        only_first_message = '''Привіт, я знаю який зараз курс валют. А ти? \nВведіть назву валюти: USD , EUR, RUR.
        \nДетальна інформація: Архів назва валюти дата.
        \nНаприклад: Архів USD 02.02.2022'''
        telegram_url = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={from_id}&text={only_first_message}'
        self.get_json(telegram_url)

    def data_time(self, text, from_id):
        a, currency, date = text.split()
        result = self.get_json(f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date}')
        for i in result['exchangeRate']:
            if currency.upper() == i.get('currency'):
                data = f"Курс {currency}: \n {date} \n {i['saleRate']} \n {i['purchaseRate']}"
                telegram_url = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={from_id}&text={data}'
                self.get_json(telegram_url)
        if not result['exchangeRate']:
            telegram_url = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={from_id}&text=Некоректно введені дані'
            self.get_json(telegram_url)

    def get_updates(self):
        update_ids = []
        update_url = f'https://api.telegram.org/bot{self.token}/getUpdates'
        while True:
            updates = self.get_json(update_url)
            last_message = updates['result'][-1]
            if last_message.get('message'):
                from_id = last_message['message']['from']['id']
                if not last_message['update_id'] in update_ids:
                    update_ids.append(last_message['update_id'])
                    if last_message['message'].get('text'):
                        optimal = last_message['message']['text'].upper()
                        if optimal in ['USD', 'EUR', 'RUR']:
                            self.send_message(optimal, from_id)
                        elif last_message['message']['text'] == '/start':
                            self.first_message(from_id)
                        elif 'архів' in last_message['message']['text'].lower():
                            self.data_time(last_message['message']['text'], from_id)

                        else:
                            text = 'Введіть назву валюти: USD , EUR, RUR.'
                            telegram_url = f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={from_id}&text={text}'
                            self.get_json(telegram_url)
            else:
                update_ids.append(last_message['update_id'])
                if not last_message['update_id'] in update_ids:
                    self.first_message(last_message['my_chat_member']['from']['id'])


activation_bot = TelegramBot('732897762', '5252793321:AAG3wJoRVlXo-SJ12trF-edZ3VIENPpIFjI')
activation_bot.get_updates()
