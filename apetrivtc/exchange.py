#!/usr/bin/env python

import argparse
from menu.menu_commands import menu


def get_default_currency():
    """
    Get the positional argument and return default currency.
    """
    parser = argparse.ArgumentParser(description='Program for working with currencies.')
    parser.add_argument('-d', '--default', type=str, metavar='',
                        help='Default currency', default='UAH', required=False)
    args = parser.parse_args()
    return args.default


if __name__ == '__main__':
    DEFAULT_CURRENCY = get_default_currency()
    menu(DEFAULT_CURRENCY)
