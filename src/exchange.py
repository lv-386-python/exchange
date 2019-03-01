import argparse

from Rate import CurrencyRate
from Timeline import today, history

parser = argparse.ArgumentParser(description='Culculate currency exchange rate')
parser.add_argument('-d', '--default', type=str, help='Default currency')
default = parser.parse_args().default
if not default:
    default = 'UAH'

rate = CurrencyRate(today, default=default)

if __name__ == '__main__':
    with open('commands.txt') as f:
        for line in f:
            print(line, end='')

    while True:
        command = input('\nPlease, write your command:\n')
        if command == 'exit()':
            exit('goodbye!')
        elif 'convert' in command:
            args = command[len('command') + 1:-1].split(',')  # get args
            rate.convert(args[0], args[1])
        elif 'set_default' in command:
            args = command[len('set_default') + 1:-1]
            default = args
            rate = CurrencyRate(today, default=default)
        elif 'show_info' in command:
            rate.show_info()
        elif 'show_history' in command:
            args = command[len('show_history') + 1:-1].split(',')
            if len(args) == 1:
                history(args[0])
            else:
                history(args[0], args[1])
        else:
            print("Sorry, unknown command.Please, try again")
