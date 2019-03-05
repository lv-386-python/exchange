from commands import (
				show_history, show_info, set_default, convert, good_bye)

CURRENCIES = []
COMMANDS = ['convert', 'help', 'history', 'set', 'q']

def menu():
    '''Displaying the menu'''
    greating = (
        '*********Hello there!*********\n'
        '***Welcome to Exchange app!***\n'
        'To use Exchange type one of the following commands:\n'
        '* [convert]\n'
        '* [help] for showing info\n'
        '* [history] for showing rate history (Input format: [currency] [sum])\n'
        '* [set] for setting default currency\n'
        '* [q] for exit\n'
                )
    return greating 


def get_answer():
    '''Getting the command from input'''
    return input('......\nPlease input the command:\n>>>>>> ')


if __name__ == "__main__":
    print(menu())
    answer = ''
    while answer != 'q':
        answer = get_answer()
        if answer == 'convert':
            convert()
        elif answer == 'help':
            show_info()
        elif answer == 'history':
            show_history()
        elif answer == 'set':
            set_default()
        elif answer == 'q':
            good_bye()
        else:
            print('!!!\nPlease repeat carefully\n')
            if get_answer() not in COMMANDS:
                get_answer()
        answer = input('Do you want to continue? [y/n]')
        if answer == 'y':
            menu()
        else:
            good_bye()
