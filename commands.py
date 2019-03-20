#!/usr/bin/env python
"""This module provides menu with all commands tщ manipulate data"""

import time
from datetime import datetime, timedelta

import requests

from utils import get_key, set_key


class ApiParser:
    ''' class to parse and manipulate data from requested url'''

    def __init__(self):
        self.url = "https://api.exchangeratesapi.io/"
        self.default_cur = get_key('DEFAULT_CUR')
        self.currencies = get_key('CURRENCIES')

    def convert(self, answer=False):
        '''Command that convert the currency.'''
        if answer is False:
            print('\n<<<<<<Please choose currencies and amount from the following:'
                  '{}\nGBP is default one>>>>>>'.format(self.currencies))
            answer = input(
                'Input format: \n[quantity] [currency] for default currency\n'
                '[quantity+currency] [currency] for converting custom currency\n>>>>>> ')
        if answer == 'q':
            quit()
        answer = answer.split()
        quantity = answer[0]
        to_exchange = answer[1].upper()
        q_currency = quantity[-3:]
        if quantity.isnumeric():
            url_parse = '{}latest?base={}&symbols={}'.format(
                self.url,
                self.default_cur,
                to_exchange)
            request = requests.get(url_parse).json()
            for value in request['rates'].items():
                amount = value[1] * int(quantity[:3])
                print(f'\nFor today {quantity} {self.default_cur} costs {round(amount, 3)} {value[0]}')
        else:
            url_parse = f'{self.url}latest?base={q_currency}&symbols={to_exchange}'
            request = requests.get(url_parse).json()
            for value in request['rates'].items():
                amount = value[1] * int(quantity[:3])
                print(f'\nFor today {quantity[:3]} {q_currency} costs {round(amount, 3)} {value[0]}')

    def show_info(self):
        '''
        Command showing the info about the default currency,
        source url and current
        currencies to work with.
        '''
        source_api = 'SOURCE: ' + self.url + '/latest'
        currencies = self.currencies
        url_parse = f'{self.url}latest?base={self.default_cur}&symbols={currencies}'
        request = requests.get(url_parse).json()
        print('\nDefault currency: ' + self.default_cur + '\n')
        for value in request['rates'].items():
            print(f'For today 1 {self.default_cur} costs {round(value[1], 3)} {value[0]}')
        print(source_api)

    def set_default(self, answer):
        '''
        Command to set default currency

        '''
        print('\n<<<<<<The list of available currencies: {}\n{} is default one>>>>>>'.format(
            self.currencies, self.default_cur))
        future_default_key = answer.upper()
        if future_default_key not in get_key('CURRENCIES'):
            print('Choose the one from the list')
            self.set_default()
            if answer == 'q':
                quit()
        set_key('DEFAULT_CUR', future_default_key)
        self.default_cur = future_default_key
        print(f'\n<<<<<<From now your default currence is {self.default_cur}.')

    def show_history(self):
        '''Command showing the history of changing the currency rate in given
        period.
        '''
        print('<<<<<< Here is the list of possible currencies: {}\n'.format(
            ', '.join([c for c in self.currencies.split(',')])))
        time.sleep(1)
        default_currency = input('>>>>>>Please choose one to follow: \n>>>>>>')
        while True:
            if default_currency not in self.currencies.split(','):
                time.sleep(1)
                default_currency = input(
                    '<<<<<<Please check you input one more time\n\n'
                    '>>>>>>Please choose one to follow: \n'
                ).upper()
            else:
                amount_of_days = input(
                    '>>>>>>Please input period [in days]: ')
                if amount_of_days.isnumeric():
                    break
            continue

        delta = int(amount_of_days)
        url_parses = [
            '{}{}?base={}&symbols={}'.format(
                self.url,
                (datetime.now() - timedelta(i)).strftime('%Y-%m-%d'),
                self.default_cur,
                self.currencies)
            for i in range(1, delta + 1)]
        responses = [requests.get(u).json() for u in url_parses]
        for resp in responses:
            print(f"For {resp['date']} rates were: \n")
            for key, value in resp['rates'].items():
                print(f'1 {self.default_cur} - {round(value, 3)} {key}')
            print()
