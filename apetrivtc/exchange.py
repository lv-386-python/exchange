#!/usr/bin/env python

"""
Main module for script launching.
"""

import argparse
from commands import menu_view


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
    menu_view(DEFAULT_CURRENCY)
