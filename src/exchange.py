'''
Main module for exchange app
'''

import argparse

from rate import CurrencyRate
from timeline import TODAY, history

PARSER = argparse.ArgumentParser(description='Culculate currency exchange rate')
PARSER.add_argument('-d', '--default', type=str, help='Default currency', default='UAH')
DEFAULT_CURRENCY = PARSER.parse_args().default

TODAY_RATE = CurrencyRate(TODAY, default=DEFAULT_CURRENCY)


def execute_command(command):
    'CLI manager'
    if 'exit' in command:
        exit('goodbye!')

    elif 'convert' in command:
        args = command[len('command') + 1:-1].split(',')
        sell = args[0]
        buy = args[1].upper()
        amount = ''
        currency_to_sell = ''
        digits = [char for char in sell if char.isdigit() or char == '.']
        amount = amount.join(digits)
        amount = float(amount)
        letters = [char for char in sell if char.isalpha()]
        if letters:
            currency_to_sell = currency_to_sell.join(letters).upper()
        else:
            currency_to_sell = TODAY_RATE.default
        TODAY_RATE.convert(amount, currency_to_sell, buy)

    elif 'set_default' in command:
        new_default = command[len('set_default') + 1:-1].upper()
        TODAY_RATE.set_default(new_default)

    elif 'show_info' in command:
        TODAY_RATE.show_info()

    elif 'show_history' in command:
        args = command[len('show_history') + 1:-1].split(',')
        if len(args) == 1:
            currency = args[0].upper()
            history(currency)
        else:
            currency = args[0].upper()
            period = int(args[1])
            history(currency, period)
    else:
        print("Sorry, unknown command.Please, try again")


if __name__ == '__main__':
    with open('commands.txt') as f:
        for line in f:
            print(line, end='')

    while True:
        COMMAND = input('\nPlease, write your command:\n')
        execute_command(COMMAND)
