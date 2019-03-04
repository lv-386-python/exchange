import requests
import datetime

URL_API = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
CURRENT = 'cc'
VALUE = 'rate'
CURRENT_COUNTRY = ['UAH', 'USD', 'EUR', 'PLN']
DEFAULT_CURRENT = CURRENT_COUNTRY[0]

def view_info(DEFAULT_CURRENT, currencies):
    print("Default current: {0}".format(DEFAULT_CURRENT))
    print("API URL: {0}".format(URL_API))

    currency_rates = get_currency(currencies)
    for currency in currencies:
        print("Today, 1 {0} = {1} UAH".format(currency, currency_rates[currency]))


def get_currency(currencies):
    request = requests.get("{0}?json".format(URL_API))
    if request.status_code != 200:
        print("Service is temporarily unavailable.")
    currency_rates = {}.fromkeys(currencies, 1)
    for i in request.json():
        if i[CURRENT] in currencies:
            currency_rates[i[CURRENT]] = (i[VALUE])
    return currency_rates


def currency_day(currency, date):
    if currency == 'UAH':
        return 1
    day = date.strftime('%Y%m%d')
    request = requests.get("{0}?valcode={1}&date={2}&json".format(URL_API, currency, day))
    if request.status_code != 200:
        print("Error maybe API doesn`t work :(")
    for i in request.json():
        if i[CURRENT] == currency:
            return i[VALUE]


def default_currency(currencies):
    while True:
        print("Choose values:")
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

def convert_currency(DEFAULT_CURRENT, currencies):
    print("'q' --- to exit.")
    print(" ".join(currencies))
    print("[sum][currency]")

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
            print("Please try again")
            continue
        if not currency:
            print("Correct : [sum] and [currency]")
            continue
        elif currency not in currencies:
            print("Incorrect input")
            continue
        currency_sum = int("".join(currency_sum))
        currency_rates = get_currency(currencies)
        result = currency_sum * currency_rates[currency] / (currency_rates[DEFAULT_CURRENT])
        print("{0} {1} = {2:.2f} {3}\n".format(currency_sum, currency, result, DEFAULT_CURRENT))


def view_history(currencies):
    print("\nEnter current and day {USD 5} (default 7 days).")
    print("Available currency:")
    print(" ".join(currencies))
    default_days = '7'
    while True:
        user_input = input("--- ")
        if user_input == 'q':
            break
        if user_input.isalpha():
            if user_input not in currencies:
                print("No such currency, try again.")
                continue
            currency, days = user_input, default_days
        elif user_input.isdigit():
            print("Your requests not good, try again.")
            continue
        else:
            currency, days =  user_input.split(" ",1)
        if not days.isdigit() or currency not in currencies:
            print("Your requests not good, try again.")
            continue
        days = int(days)
        for i in range(days):
            day = datetime.date.today() - datetime.timedelta(i)
            rate = currency_day(currency, day)
            print("On {0} 1 {1} = {2} UAH".format(day, currency, rate))


def main_menu_system():
    print("\n---------- MAIN MENU EXCHANGE SYSTEM ----------")
    print("\n1. Show info.")
    print("\n2. Show default currency.")
    print("\n3. Convert currency.")
    print("\n4. Show history.")
    print("\nq. Quit.\n")

PRESS_USER = ''

if __name__ == '__main__':
    main_menu_system()
    while PRESS_USER != 'q':
        PRESS_USER = input("--- Press count: ")
        main_menu_system()
        if PRESS_USER == '1':
            view_info(DEFAULT_CURRENT, CURRENT_COUNTRY)
        elif PRESS_USER == '2':
            default_currency = default_currency(CURRENT_COUNTRY)
            main_menu_system()
        elif PRESS_USER == '3':
            convert_currency(DEFAULT_CURRENT, CURRENT_COUNTRY)
            input("Press -> 'enter' to main menu")
            main_menu_system()
        elif PRESS_USER == '4':
            view_history(CURRENT_COUNTRY)
            input("Press -> 'enter' to main menu")
            main_menu_system()
        elif PRESS_USER == 'q':
            print("\nGood buy\n")
            break
        else:
            print("\nIts not correct!\n")
