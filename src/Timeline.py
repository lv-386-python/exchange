import datetime

from Rate import CurrencyRate, to_fixed


def date_for_api(date):
    day = str(date.day).rjust(2, '0')
    month = str(date.month).rjust(2, '0')
    formated_for_api = f'{day}.{month}.{date.year}'
    return formated_for_api


today = date_for_api(datetime.date.today())


def history(currency: str, num=3):
    num = int(num)
    currency = currency.upper()
    days = list(map(date_for_api,
                    [datetime.datetime.today() - datetime.timedelta(days=i) for i in range(num)]))

    exchange_records = [CurrencyRate(day).get_rate(currency) for day in days]

    deltas = [0, ]  # initial delta should be zero
    deltas += [to_fixed(exchange_records[i] - exchange_records[i - 1]) for i in range(num - 1)]

    print('History of currency rate and changes:')
    for i in range(num):
        print(f'{days[i]}:  exchage rate {exchange_records[i]}, delta = {deltas[i]}')
