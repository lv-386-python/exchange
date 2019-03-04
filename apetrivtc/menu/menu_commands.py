"""
Set of functions for using in menu.
"""

import datetime
import os
import requests

JSON_API = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
CURRENCY_LIST = ['UAH', 'USD', 'EUR', 'PLN']
CURRENCY_CODE_IN_JSON = 'cc'


def display_title_bar():
    """
    Displays a title bar and menu.
    """
    print("\t**********************************************")
    print("\t***               EXCHANGE.PY              ***")
    print("\t**********************************************")
    print()
    print("Please choose one of the following commands:\n")
    print("\tMAIN MENU")
    print("\t[1] - Show general info.")
    print("\t[2] - Set default currency.")
    print("\t[3] - Convert currency.")
    print("\t[4] - Show exchange rate history for currency.")
    print("\t[q] - Quit.\n")


def get_user_choice():
    """
    Get user input.
    """
    return input("What would you like to do? ")


def menu(default_currency):
    """
    Launches and processes the menu.
    """
    choice = ''
    os.system('clear')
    display_title_bar()
    # Set up a loop where users can choose what they'd like to do.
    while choice != 'q':
        choice = get_user_choice()
        os.system('clear')
        display_title_bar()
        # Respond to the user's choice.
        if choice == '1':
            info = show_info(default_currency, CURRENCY_LIST)
            print(info)
        elif choice == '2':
            default_currency = set_default_currency(CURRENCY_LIST)
            os.system('clear')
            display_title_bar()
        elif choice == '3':
            convert_currency(default_currency, CURRENCY_LIST)
            input("Please press enter to continue.")
            os.system('clear')
            display_title_bar()
        elif choice == '4':
            show_history(CURRENCY_LIST)
            input("Please press enter to continue.")
            os.system('clear')
            display_title_bar()
        elif choice == 'q':
            print("\nThanks for visiting!\n")
        else:
            print("\nI didn't understand that choice.\n")


def show_info(default_currency, currencies):
    """
    Returns exchange rate for currencies.
    """
    info = f"Default currency: {default_currency}\n"
    info += f"JSON_API URL: {JSON_API}\n"
    currency_rates = get_currency_rates(currencies)
    for currency in currencies:
        info += f"Today, 1 {currency} = {currency_rates[currency]:.2f} UAH\n"
    return info


def get_currency_rates(currencies):
    """
    Returns dictionary with currency rates.
    """
    request = requests.get(f"{JSON_API}?json")
    if request.status_code != 200:
        print("Service is temporarily unavailable.")
    currency_rates = {}.fromkeys(currencies, 1)
    for item in request.json():
        if item['CURRENCY_CODE_IN_JSON'] in currencies:
            currency_rates[item['CURRENCY_CODE_IN_JSON']] = (item['rate'])
    return currency_rates


def get_currency_rate_per_day(currency, date):
    """
    Returns dictionary with currency rates for a certain day.
    """
    if currency == 'UAH':
        return 1
    day = date.strftime('%Y%m%d')
    request = requests.get(f"{JSON_API}?valcode={currency}&date={day}&json")
    if request.status_code != 200:
        return "Service is temporarily unavailable."
    for item in request.json():
        if item['CURRENCY_CODE_IN_JSON'] == currency:
            return item['rate']
        return None


def set_default_currency(currencies):
    """
    Sets default currency from the currency list.
    """
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
        print("Please choose correct value.")


def convert_currency(default_currency, currencies):
    """
    Converts currency by exchange rate.
    """
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
        currency_rates = get_currency_rates(currencies)
        result = currency_sum * currency_rates[currency] / (currency_rates[default_currency])
        print(f"{currency_sum} {currency} = {result:.2f} {default_currency}\n")


def show_history(currencies):
    """
    Show history of exchange rate of chosen currency.
    By default shows a course of 3 days.
    """
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
            currency, days = user_input.split(" ", 1)
        if not days.isdigit() or currency not in currencies:
            print("Incorrect input. Please try again.")
            continue
        days = int(days)
        for i in range(days):
            day = datetime.date.today() - datetime.timedelta(i)
            rate = get_currency_rate_per_day(currency, day)
            print(f"On {day} 1 {currency} = {rate:.2f} UAH")
