#!/usr/bin/env python
'''Initialization module having menu launcher '''

import argparse
from os import get_terminal_size
from commands import ApiParser

COMMANDS = ApiParser()
PARSER = argparse.ArgumentParser(description='Simple console app for converting currencies.')
PARSER.add_argument('-i', action='store_true',
                    help='''Showing info about the default currency, source url and current
                    currencies to work with''')
PARSER.add_argument('-d', action='store', help='''Type currency to set as default''')
PARSER.add_argument('-c', action='store', help=''''Input format: \n[quantity] [currency] for default currency\n'
                    '[quantity+currency] [currency] for converting custom currency\n>>>>>> ''')


def menu():
    '''Displaying the menu'''
    greating = (
        '\n*********Hello there!*********\n'
        '***Welcome to Exchange app!***\n'
        'To use Exchange type one of the following commands:\n'
        '1) [convert]\n'
        '2) [help] for showing info\n'
        '3) [history] for showing rate history (Input format: [currency] [sum])\n'
        '4) [set] for setting default currency\n'
        '5) [q] for exit\n'
    )
    print(greating)


def get_answer():
    '''Getting the command from input'''
    return input('......\nPlease input the command:\n>>>>>> ')


def good_bye():
    '''
    Command to quit the program and printing Good bye message.
    '''
    good_bye_message = 'Thank you for using Exchange app. Take care.'
    print(good_bye_message.center(get_terminal_size()[0], '*'))


if __name__ == "__main__":
    ARGS = PARSER.parse_args()
    if ARGS.i is True:
        COMMANDS.show_info()
    if ARGS.d:
        COMMANDS.set_default(ARGS.d)
    if ARGS.c:
        COMMANDS.convert(answer=ARGS.c)
    else:
        while True:
            menu()
            answer = get_answer()
            if answer in ['convert', '1']:
                try:
                    COMMANDS.convert()
                except IndexError:
                    COMMANDS.convert()
            elif answer in ['help', '2']:
                COMMANDS.show_info()
            elif answer in ['history', '3']:
                COMMANDS.show_history()
            elif answer in ['set', '4']:
                answer = input('>>>>>>Please input the currency that you want to setup as default\n>>>>>> ')
                COMMANDS.set_default(answer)
            elif answer == 'q':
                good_bye()
                break
            else:
                print('\n!!!\nНерпавильна комманда\n')
