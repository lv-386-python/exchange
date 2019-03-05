from datetime import datetime, timedelta
import time
import requests
import json


CORE_API = "https://api.exchangeratesapi.io/"
CURRENCIES = ['GBP', 'USD', 'EUR', 'CAD']


def convert():
	'''Command that will be used to converts currency.'''
	print('<<<<<<Please choose currencies and amount from the following: \n'
		'\n {}, {}, {}\n\n GBP is default one>>>>>>'.format(
					*CURRENCIES[1:]))
	answer = input(
		'Input format: \n[quantity] [currency] for default currency\n'
		'[quantity+currency] [currency] for converting custom currency\n>>>>>> ')
	answer = answer.split()
	quantity = answer[0]
	to_exchange = answer[1].upper()
	print(quantity[:3])
	if quantity.isnumeric():
		url_parse = f'{CORE_API}latest?base={CURRENCIES[0]}&symbols={to_exchange}'
		request = requests.get(url_parse).json()
		for v in request['rates'].items():
			print(f'For today {quantity} {CURRENCIES[0]} costs {v[1]*int(quantity[:3])} {v[0]}')
	else:
		url_parse = f'{CORE_API}latest?base={quantity[-3:]}&symbols={to_exchange}'
		request = requests.get(url_parse).json()
		for v in request['rates'].items():
			print(f'For today {quantity[:3]} {quantity[-3:]} costs {v[1]*int(quantity[:3])} {v[0]}')


def show_info():
	'''
	Command showing the info about the default currency,
	source url and current
	currencies to work with.
	Returns:
			Nessesary info to start converting proccess.
	'''
	source_api = 'SOURCE: ' + CORE_API + '/latest'
	currencies = ','.join(i for i in CURRENCIES[1:])
	url_parse = f'{CORE_API}latest?base={CURRENCIES[0]}&symbols={currencies}'
	request = requests.get(url_parse).json()
	for v in request['rates'].items():
		print(f'For today 1 {CURRENCIES[0]} costs {v[1]} {v[0]}')
	print('\n')
	print('Default currency: ' + CURRENCIES[0] + '\n')
	print(source_api)


def show_history():
	'''Command showing the history of changing the currency rate in given
	period.
	'''
	print('<<<<<<Here is the list of possible currencies:\n {}, {}, {}, {}'.format(*CURRENCIES))
	time.sleep(1)
	default_currency = input('>>>>>>Please choose one to follow: ')
	while True:
		if default_currency not in CURRENCIES:
			time.sleep(1)
			default_currency = input(
				'<<<<<<Please check you input one more time\n\n'
				'>>>>>>Please choose one to follow: \n'
				).upper()
		else:
			amount_of_days = input(
				'>>>>>>Please input period [in days]: '
				)
			if amount_of_days.isnumeric():
				break
		continue
	period = datetime.today() - timedelta(int(amount_of_days))
	period = period.strftime('%Y-%m-%d')
	available_currencies = ','.join(i for i in CURRENCIES)
	url_parse = f'{CORE_API}{period}?base={default_currency}&symbols={available_currencies}'
	request = requests.get(url_parse).json()
	print(request)
	for k, v in request['rates'].items():
		print(f'{k} - {v}') 


def set_default():
	'''
	Command to set default currency
	Args:
			param1: str, currency to set as default
	Returns:
			Info about changes that was done.
	'''
	default_currency = input(
		'>>>>>>Plese input the currency that you want to setup as default\n>>>>>>')
	default_currency = default_currency.upper()
	while True:
		if default_currency in CURRENCIES:
			break
		else:
			default_currency = input(
				'>>>>>>Please choose one from the list\n {}, {}, {}, {}\n>>>>>>'.format(
					*CURRENCIES))
	del CURRENCIES[0]
	CURRENCIES.insert(0, default_currency)
	print(f'<<<<<<From now your default currence is {default_currency}.')


def good_bye():
	'''
	Command to quit the program and printing Good bye message.
	''' 
	good_bye_message = 'Thank you for using Exchange app. Take care.'
	print(good_bye_message.center(get_terminal_size()[0], '*'))
	sys.exit()
