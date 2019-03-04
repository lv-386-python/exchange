import requests
import datetime

API = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"


def view_info(default_currency, currencies):
    print("Default currency: {0}".format(default_currency))
    print("API URL: {0}".format(API))

    currency_rates = get_currency(currencies)
    for currency in currencies:
        print("Today, 1 {0} = {1} UAH".format(currency, currency_rates[currency]))


def get_currency(currencies):
    request = requests.get("{0}?json".format(API))
    if request.status_code != 200:
        print("Service is temporarily unavailable.")
    currency_rates = {}.fromkeys(currencies, 1)
    for i in request.json():
        if i['cc'] in currencies:
            currency_rates[i['cc']] = (i['rate'])
    return currency_rates


def get_currency_rate_per_day(currency, date):
    if currency == 'UAH':
        return 1
    day = date.strftime('%Y%m%d')
    request = requests.get("{0}?valcode={1}&date={2}&json".format(API, currency, day))
    if request.status_code != 200:
        print("Service is temporarily unavailable.")
    for i in request.json():
        if i['cc'] == currency:
            return i['rate']


def default_currency(currencies):
    while True:
        print("Please choose from the next values:")
        for choice, currency in enumerate(currencies, 1):
            print("\t[{0}] - {1}.".format(choice, currency))
        user_input = input("--- ")
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
        user_input = input("--- ")
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
            print("Write : [sum] and current: [currency]")
            continue
        elif currency not in currencies:
            print("No currency")
            continue
        currency_sum = int("".join(currency_sum))
        currency_rates = get_currency(currencies)
        result = currency_sum * currency_rates[currency] / (currency_rates[default_currency])
        print("{0} {1} = {2} {3}\n".format(currency_sum, currency, result, default_currency))


def view_history(currencies):
    print("\n\nPlease enter currency and number of days (default 3).")
    print("Available currency:")
    print(" ".join(currencies))
    print("Currency,sum like that {USD 10}")
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
            print("On {0} 1 {1} = {2} UAH".format(day, currency, rate))

CURRENCT_COUNTRY = ['UAH', 'USD', 'EUR', 'PLN']


def main_menu_system():
    print("\n---------- MAIN MENU EXCHANGE SYSTEM ----------")
    print("\n1. Show general info.")
    print("\n2. Set default currency.")
    print("\n3. Convert currency.")
    print("\n4. Show exchange rate history for currency.")
    print("\nq. Quit.\n")


def get_user_choice():
    return input(">>> Press count: ")


default_current = CURRENCT_COUNTRY[0]
press_user = ''

if __name__ == '__main__':
    main_menu_system()
    while press_user != 'q':
        press_user = get_user_choice()
        main_menu_system()
        if press_user == '1':
            view_info(default_current, CURRENCT_COUNTRY)
        elif press_user == '2':
            default_currency = default_currency(CURRENCT_COUNTRY)
            main_menu_system()
        elif press_user == '3':
            convert_currency(default_current, CURRENCT_COUNTRY)
            input("Please press enter to continue.")
            main_menu_system()
        elif press_user == '4':
            view_history(CURRENCT_COUNTRY)
            input("Please press enter to continue.")
            main_menu_system()
        elif press_user == 'q':
            print("\nThanks for visiting!\n")
            break
        else:
            print("\nI didn't understand that choice.\n")
