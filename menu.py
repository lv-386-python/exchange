"""
This module demonstrate currency exchange
"""
import argparse
import requests
from _datetime import datetime, timedelta

PARSER = argparse.ArgumentParser(description='Exchange rate')
PARSER.add_argument('-s', '--sum', type=int, help='How much money', default=100)
PARSER.add_argument('-f', '--from_what', type=str, help='Default currency', default='UAH')
PARSER.add_argument('-t', '--to_what', type=str, help='Default currency', default='USD')
ARGS = PARSER.parse_args()
KEYS = ['USD', 'UAH', 'EUR', 'PLN', 'AUD', 'CHF', 'GBP', 'RUB', 'CZK']
BASE = "https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&apikey=XA2HBR8XZOX50BK7"
FOR_HISTORY = "https://www.alphavantage.co/query?function=FX_DAILY&apikey=XA2HBR8XZOX50BK7"
DAYS = 3
FROM_CURRENCY = "&from_currency="
TO_CURRENCY = "&to_currency="
FROM_SYMBOL = "&from_symbol="
TO_SYMBOL = "&to_symbol="
NAME = 'Realtime Currency Exchange Rate'
EXC_STR = '5. Exchange Rate'
DATE_STR = 'Time Series FX (Daily)'

def show_info(from_value, to_value):
    """
    This function demonstrates information about currencies
    :param from_value: From what currency you want to change money
    :param to_value: To what currency you want to change money
    :return: Dictionary with currency values
    """
    current_api = BASE + FROM_CURRENCY + from_value + TO_CURRENCY + to_value
    print(f"Current API URL: {current_api} ")
    all_currencies = requests.get(f'{current_api}').json()
    currency_dict = all_currencies[NAME][EXC_STR]
    print(f"{from_value} - {to_value} {currency_dict}")
    return currency_dict

def show_history(from_value, to_value):
    """
    This function demostrates history of currency exchange values
    :param from_value: From what currency you want to change money
    :param to_value: To what currency you want to change money
    """
    if from_value == 'UAH':
        print("Sorry, it doesn't work for UAH, please choose smth else ")
        show_menu()
    else:
        current_api = FOR_HISTORY + FROM_SYMBOL + from_value + TO_SYMBOL + to_value
        all_currencies = requests.get(f'{current_api}').json()
        currency_dict = all_currencies[DATE_STR]
        print(current_api)
        for i in range(DAYS):
            print(f"For {(datetime.now() - timedelta(days=i-1)).strftime('%Y-%m-%d')} \n"
                  f" {currency_dict[(datetime.now() - timedelta(days=i-1)).strftime('%Y-%m-%d')]}")

def set_default(val_list):
    """
    This function used to set new currency values
    :param val_list: list of available currencies
    """
    from_value = input("What currency do you want to change? Please, write in format like USD ")
    to_value = input("To what currency do you want to change? Please, write in format like USD ")
    amount = int(input("Print new amount of your value "))
    ARGS.sum = amount
    if from_value and to_value in val_list:
        ARGS.from_what = from_value
        ARGS.to_what = to_value
        print(f'[{from_value}] AND [{to_value}] ARE DEFAULT VALUES, SUM = {amount}')
    else:
        ARGS.from_what = 'UAH'
        ARGS.to_what = 'UAH'
        print(f'[{from_value}] AND [{to_value}]  ARE DEFAULT, SUM = {amount}')

def convert(from_value, to_value, amount):
    """
    This function convert currencies
    :param from_value: From what currency you want to change money
    :param to_value: To what currency you want to change money
    :param amount: Amoun of money which to change
    """
    current_api = BASE + FROM_CURRENCY + from_value + TO_CURRENCY + to_value
    all_currencies = requests.get(f'{current_api}').json()
    currency_sum = round(float(all_currencies[NAME][EXC_STR]), 3)
    print(f"Converted sum from [{from_value}] to [{to_value}] = {round(currency_sum*amount,3)}"
          f" and Exchange Rate = {currency_sum}")

def show_menu():
    """
    This function demonstrates menu
    """
    print("**************************************************")
    print("*****    Main Choice: Choose 1 of 5 choices  *****")
    print(f"*****          Default value is {ARGS.from_what}          *****")
    print("*****     Choose [1] to convert money        *****")
    print("*****  Choose [2] to set other default value *****")
    print("Choose [3] to show information about currencies")
    print("*****      Choose [4] to show history        *****")
    print("*******        Choose [5] to exit          *******")
    choice = input("What are you want to do? ")
    if choice == "5":
        print("******       Bye!!!         ******")
    elif choice == "4":
        show_history(ARGS.from_what, ARGS.to_what)
        show_menu()
    elif choice == "3":
        show_info(ARGS.from_what, ARGS.to_what)
        show_menu()
    elif choice == "2":
        set_default(KEYS)
        show_menu()
    elif choice == "1":
        convert(ARGS.from_what, ARGS.to_what, ARGS.sum)
        show_menu()
    else:
        print("I don't understand your choice. Choose 1 of 5 choices ")
        show_menu()

if __name__ == '__main__':
    show_menu()
