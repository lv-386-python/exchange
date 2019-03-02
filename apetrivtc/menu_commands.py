import requests
import datetime


API = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"


def show_info(default_currency, currencies):
    print(f"Default currency: {default_currency}")
    print(f"API URL: {API}")

    currency_rates = get_currency_rates(currencies)
    for currency in currencies:
        print(f"Today, 1 {currency} = {currency_rates[currency]:.2f} UAH")


def get_currency_rates(currencies):
    request = requests.get(f"{API}?json")
    if request.status_code != 200:
        print("Service is temporarily unavailable.")
    #print("request.status_code", request.status_code)
    currency_rates = {}.fromkeys(currencies, 1)
    for i in request.json():
        if i['cc'] in currencies:
            currency_rates[i['cc']] = (i['rate'])
    #print(currency_rates)
    return currency_rates


def get_currency_rate_per_day(currency, date):
    if currency == 'UAH':
        return 1
    day = date.strftime('%Y%m%d')
    request = requests.get(f"{API}?valcode={currency}&date={day}&json")
    if request.status_code != 200:
        print("Service is temporarily unavailable.")
    #print("request.status_code", request.status_code)
    for i in request.json():
        if i['cc'] == currency:
            return i['rate']


def set_default_currency(currencies):
    while True:
        print("Please choose from the next values:")
        for choice, currency in enumerate(currencies, 1):
            print(f"\t[{choice}] - {currency}.")
        user_input = input(">>> ")
        if not user_input.isdigit():
            print("Please enter only digits.")
            continue
        number = int(user_input)
        if number in dict(enumerate(currencies, 1)):
            return dict(enumerate(currencies, 1))[number]
        else:
            print("Please choose correct value.")

def convert_currency(default_currency, currencies):
    print("\n\nPlease enter sum of currency and currency for converting.")
    print("Or press 'q' to exit.")
    print("Available currency:")
    print(" ".join(currencies))
    print("Input format: [sum][currency]")

    while True:
        user_input = input(">>> ")
        if user_input == 'q':
            break
        currency_sum = []
        currency = ""
        if user_input[0].isdigit():
            for i in user_input:
                if i.isdigit():
                    currency_sum += i
                elif i.isalpha():
                    currency += i
        else:
            print("Incorrect input. Please try again.")
            continue
        if not currency:
            print("Please see input format:")
            print("Input format: [sum][currency]")
            continue
        elif currency not in currencies:
            print("No such currency")
            continue
        currency_sum = int("".join(currency_sum))
        # print('currency_sum', currency_sum)
        # print('currency', currency)
        currency_rates = get_currency_rates(currencies)
        result = currency_sum * currency_rates[currency] / (currency_rates[default_currency])
        print(f"{currency_sum} {currency} = {result:.2f} {default_currency}\n")


def show_history(currencies):
    print("\n\nPlease enter currency and number of days (default 3).")
    print("Or press 'q' to exit.")
    print("Available currency:")
    print(" ".join(currencies))
    print("Input format: [currency] [sum]")
    default_days = '3'
    while True:
        user_input = input(">>> ")
        if user_input == 'q':
            break
        if user_input.isalpha():
            if user_input not in currencies:
                print("No such currency. Please try again.")
                continue
            currency, days = user_input, default_days
        elif user_input.isdigit():
            print("Incorrect input. Please try again.")
            continue
        else:
            currency, days =  user_input.split(" ",1)
        if not days.isdigit() or currency not in currencies:
            print("Incorrect input. Please try again.")
            continue
        days = int(days)
        for i in range(days):
            day = datetime.date.today() - datetime.timedelta(i)
            rate = get_currency_rate_per_day(currency, day)
            print(f"On {day} 1 {currency} = {rate:.2f} UAH")














