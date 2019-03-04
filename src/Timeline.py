import datetime

from Rate import CurrencyRate


def date_for_api(date):
    if date.weekday() == 0 and date.hour < 12:
        date = date - datetime.timedelta(days=1)

    day = str(date.day).rjust(2, '0')
    month = str(date.month).rjust(2, '0')
    year = date.year
    formatted_for_api = f'{year}{month}{day}'
    return formatted_for_api


TODAY = date_for_api(datetime.datetime.today())


def history(currency, period=3):
    period = int(period)
    days = list(map(date_for_api,
                    [datetime.datetime.today() - datetime.timedelta(days=days_ago)
                     for days_ago in range(period)]))

    exchange_records = [CurrencyRate(day).get_rate(currency) for day in days]

    print(f'History of {currency} rate:')
    for day in range(period):
        print(f'{days[day]}:  exchange rate {exchange_records[day]}')
