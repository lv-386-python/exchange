#!/usr/bin/env python
import requests
import argparse
from datetime import datetime, date
import calendar
import json

parser = argparse.ArgumentParser(description='Converter')
parser.add_argument('fc', type=str, help='Which currency you want to convert')
parser.add_argument('tc', type=str, help='In which currency you want to convert')

parser.add_argument('-set_default', '--default', type=str, help='Setting the default currency', default='UAH')
parser.add_argument('-convert', '--convert', help='Performs converting the currencies', action="store_true")
parser.add_argument('-history', '--history', help='Show history of the realtime exchange rate', action='store_true')
parser.add_argument('-info', '--info', help='Show information about currencies', action='store_true')
parser.add_argument('am', type=int, help='The amount you want to convert')

args = parser.parse_args()


api_base = r"https://www.alphavantage.coh/query?function=".rstrip("/")
api_key = "YENYAV2LN1O6X72E"

session = requests.Session()


def convert(from_currency, to_currency, amount):

    from_currency.upper()
    to_currency.upper()
    function = "CURRENCY_EXCHANGE_RATE"
    url = api_base+function+'&from_currency='+from_currency+'&to_currency='+to_currency+'&apikey='+api_key
    request = requests.Request("GET", url)
    prepared = request.prepare()
    response = session.send(prepared)
    json_exc = response.json()
    return(round(float(float(json_exc['Realtime Currency Exchange Rate']['5. Exchange Rate'])*amount),3))



def show_information(json_exc):
    timestamp = datetime.fromtimestamp(json_exc['meta']['timestamp'])
    return (timestamp.strftime('%Y-%m-%d %H:%M:%S'))
    #my_date = date.today()
    #calendar.day_name[my_date.weekday()


def show_history(from_currency, to_currency):
    function = "FX_DAILY"
    url = api_base+function+"&from_symbol="+from_currency.upper()+"&to_symbol="+to_currency.upper()+"&apikey="+api_key
    request = requests.Request("GET", url)
    prepared = request.prepare()
    response = session.send(prepared)
    json_exc = response.json()
    got_dict = dict(json.dumps(json_exc))
    #time_series = (json_exc["Time Series FX (Daily)"]).keys()
    #sorted_by_value = sorted(time_series.items(), key=lambda kv: kv[0])
    #print(sorted_by_value[0:3])
    print(got_dict)


def set_default_currency():
    pass


if __name__ == '__main__':
        if args.convert:
            print(
                "The result of conversion from {} to {} with amount {} is {}".format(args.fc, args.tc, args.am,
                                                                                     convert(args.fc, args.tc,
                                                                                             args.am)))
        elif args.history:
            print("The daily time series of the {} and {}, updated realtime".format(args.fc, args.tc,
                                                                                    show_history(args.fc, args.tc)))

        elif args.set_default:
            print("")

