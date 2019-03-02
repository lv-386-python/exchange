#!/usr/bin/env python

import os
from menu_commands import (show_info, set_default_currency,
                            convert_currency, show_history)

CURRENCIES = ['UAH', 'USD', 'EUR', 'PLN']


### FUNCTIONS ###

def display_title_bar():
    """
    Clears the terminal screen, and displays a title bar and menu.
    """
    os.system('clear')
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
    return input("What would you like to do? ")


### MAIN PROGRAM ###

default_currency = CURRENCIES[0]
choice = ''
if __name__ == '__main__':
    # Set up a loop where users can choose what they'd like to do.
    display_title_bar()
    while choice != 'q':
        choice = get_user_choice()
        display_title_bar()
        # Respond to the user's choice.
        if choice == '1':
            show_info(default_currency, CURRENCIES)
        elif choice == '2':
            default_currency = set_default_currency(CURRENCIES)
            display_title_bar()
        elif choice == '3':
            convert_currency(default_currency, CURRENCIES)
            input("Please press enter to continue.")
            display_title_bar()
        elif choice == '4':
            show_history(CURRENCIES)
            input("Please press enter to continue.")
            display_title_bar()
        elif choice == 'q':
            print("\nThanks for visiting!\n")
        else:
            print("\nI didn't understand that choice.\n")

