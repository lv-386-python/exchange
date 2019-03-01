import requests

PRIVAT_API = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='


def to_fixed(num, digits=2):
    fixed = f"{num:.{digits}f}"
    return float(fixed)


class CurrencyRate:
    def __init__(self, date, default="UAH"):
        self._UAH = 1
        self.date = date

        res = requests.get(f'{PRIVAT_API}{date}').json()  # make request to API

        all_currencies = res['exchangeRate'][1:]  # all rates except first
        self._USD = list(filter(lambda d: d['currency'] == "USD", all_currencies))[0]['saleRate']
        self._EUR = list(filter(lambda d: d['currency'] == "EUR", all_currencies))[0]['saleRate']
        self._PLZ = list(filter(lambda d: d['currency'] == "PLZ", all_currencies))[0]['saleRate']
        self.default = default

    def get_rate(self, currency):
        currency = f'_{currency.upper()}'
        return self.__dict__[currency]

    def convert(self, sell: str, buy: str):
        amount = ''  # 'zero' string
        currency_to_sell = ''
        digits = [char for char in sell if char.isdigit() or char == '.']
        amount = amount.join(digits)
        amount = float(amount)
        letters = [char for char in sell if char.isalpha()]
        if letters:
            currency_to_sell = currency_to_sell.join(letters)
        else:
            currency_to_sell = self.default

        exchange_rate = self.get_rate(currency_to_sell) / self.get_rate(buy)
        print(f'****  You can buy {to_fixed(amount * exchange_rate)}{buy.upper()}', end='')

    def show_info(self):
        info = f'''\tDefault currency : {self.default},\n
        available currencies : 'UAH', 'USD', 'EUR', 'PLZ', \n
        API URL : {f'{PRIVAT_API}{self.date}'} '''
        print(info)
