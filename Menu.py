import argparse
import requests
from _datetime import datetime,timedelta,date
parser = argparse.ArgumentParser(description= 'Exchange rate')
parser.add_argument('-s', '--sum', type = int, help = 'How much money')
parser.add_argument('-v','--val', type = str, help = 'Default currency')
args = parser.parse_args()
keys = (['USD', 'UAH','EUR', 'PLN'])
BASE_USD = "http://apilayer.net/api/live?access_key=b9ebad6aece424e7c727772c5a9e78cb&currencies=EUR,UAH,PLN&source=USD&format=1"
BASE_UAH = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

def show_info(par,ls):
    if par == 'USD':
        print(f"Current API URL: {BASE_USD} ")
        all_currencies = requests.get(f'{BASE_USD}').json()
        usd_dict = all_currencies['quotes'].copy()
        print(usd_dict)
        return usd_dict
    else:
        print(f"Current API URL: {BASE_UAH} ")
        all_currencies = requests.get(f'{BASE_UAH}').json()
        uah_dict = {}.fromkeys(ls, 1)
        for el in all_currencies:
            if el['cc'] in ls: uah_dict[el['cc']] = (el['rate'])
        print(uah_dict)
        return uah_dict

def show_history(par,ls):
    current_time = datetime.now().strftime('%Y-%m-%d')
    current_time1 = datetime.now().strftime('%Y%m%d')
    if par == 'USD':
        print("USD values for last 3 days")
        hist_usd = "http://apilayer.net/api/live?access_key=b9ebad6aece424e7c727772c5a9e78cb&currencies=EUR,UAH,PLN&source=USD&format=1&date="
        hist_time1 = hist_usd + current_time
        hist_time2 = hist_usd + (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        hist_time3 =  hist_usd + (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
        USD1 = requests.get(f'{hist_time1}').json()
        USD1 = USD1['quotes'].copy()
        USD2 = requests.get(f'{hist_time2}').json()
        USD2 = USD2['quotes'].copy()
        USD3 = requests.get(f'{hist_time3}').json()
        USD3 = USD3['quotes'].copy()
        print(f"\t\tToday is {current_time} \n  {USD1} \n "
              f"Yesterday:  {USD2} \n  Day before yesterday: {USD3}")
    else:
        hist_uah = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json&date="
        uah_time1 = hist_uah + current_time1
        uah_time2 = hist_uah + (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        uah_time3 =  hist_uah + (datetime.now() - timedelta(days=2)).strftime('%Y%m%d')
        all_uah = requests.get(f'{uah_time1}').json()
        uah_dict1 = {}.fromkeys(ls, 1)
        for el in all_uah:
            if el['cc'] in ls: uah_dict1[el['cc']] = (el['rate'])
        all_uah2 = requests.get(f'{uah_time2}').json()
        uah_dict2 = {}.fromkeys(ls, 1)
        for el in all_uah2:
            if el['cc'] in ls: uah_dict2[el['cc']] = (el['rate'])
        all_uah3 = requests.get(f'{uah_time3}').json()
        uah_dict3 = {}.fromkeys(ls, 1)
        for el in all_uah3:
            if el['cc'] in ls: uah_dict3[el['cc']] = (el['rate'])
        print(f"\t\tToday is {current_time} \n  {uah_dict1} \n "
              f"Yesterday:  {uah_dict2} \n  Day before yesterday: {uah_dict3}")

def convert(count, currency,ls):
    prefered_currency = input("What do you want to buy?  UAH USD EUR PLN \n")
    if currency == 'USD':
        all_currencies = requests.get(f'{BASE_USD}').json()
        usd_dict = all_currencies['quotes'].copy()
        sum = usd_dict.get(currency+prefered_currency)*count
        print(sum)
    else:
        all_currencies = requests.get(f'{BASE_UAH}').json()
        uah_dict = {}.fromkeys(ls, 1)
        for el in all_currencies:
            if el['cc'] in ls: uah_dict[el['cc']] = (el['rate'])
        sum = uah_dict.get(prefered_currency)/count
        print(sum)

def show_menu():
    print("*****Main Choice: Choose 1 of 5 choices*****")
    print(f"*****Default value is {args.val}*****")
    print("Choose 1 to convert money")
    print("Choose 2 to set other default value")
    print("Choose 3 to show information about currencies")
    print("Choose 4 to show history")
    print('Choose 5 to exit')
    choice = input("What are you want to do? ")
    if choice == "5":
        print("\t\tBye!!!")
    elif choice == "4":
        show_history(args.val,keys)
        show_menu()
    elif choice == "3":
        show_info(args.val,keys)
        show_menu()
    elif choice == "2":
        set_default()
        show_menu()
    elif choice == "1":
        convert(args.sum, args.val,keys)
        print("Convert")

        show_menu()
    else:
        print("I don't understand your choice.Choose 1 of 5 choices ")
        show_menu()


def set_default():
    setted = input("What currency do you want to change? Please, write USD or UAH ")
    if setted == 'USD':
        args.val ='USD'
        print('USD IS DEFAULT')
        all_currencies = requests.get(f'{BASE_USD}').json()
    else:
        print("UNKNOWN CURRENCY\n UAH by default")
        args.val = 'UAH'
        print('UAH IS DEFAULT')
        all_currencies = requests.get(f'{BASE_UAH}').json()
    return setted

if __name__ == '__main__':
    show_menu()
