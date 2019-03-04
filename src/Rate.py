import requests

NBU_API = f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?'
AVAILABLE_CURRENCIES = {'USD', 'EUR', 'PLN', 'UAH'}


class CurrencyRate:
    def __init__(self, date, default='UAH'):
        self.date = date
        self.default = default

    @staticmethod
    def make_request(currency, date):
        request_url = f'{NBU_API}valcode={currency}&date={date}&json'
        response = requests.get(request_url).json()
        rate = float(response[0]['rate'])
        return round(rate, 2)

    def get_rate(self, currency):
        if not currency.upper() in AVAILABLE_CURRENCIES:
            print(f"No data for currency {currency}")
            return None

        if currency.upper() == 'UAH':
            return 1

        return self.make_request(currency, self.date)

    def convert(self, amount, sell, buy):
        exchange_rate = self.get_rate(sell) / self.get_rate(buy)
        result = amount * exchange_rate
        print(f'\tYou can buy {round(result, 2)} {buy.upper()}', end='')

    def show_info(self):
        info = f'''\tDefault currency : {self.default},\n
        available currencies : {AVAILABLE_CURRENCIES},\n
        API URL : {NBU_API} '''
        print(info)

    def set_default(self, new_default):
        self.default = new_default.upper()
