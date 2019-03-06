'''
module for convert, history and setings
'''
from datetime import date
import requests


DEFAULT_VALCODE = 'UAH'
DEFAULT_HISTORY_LEN = 7
NAMES_OF_FUNCTIONS = {'Convert': ['convert', '0', 'c'],
                      'Info': ['info', '1', 'i'],
                      'Showhistory': ['showhistory', '2', 'h', 'history'],
                      'Setup': ['setup', '3', 's'],
                      'Beck': ['2', 'beck'],
                      'Valute': ['0', 'valute'],
                      'Len': ['1', 'len']}
EXIT = ['4', 'exit']
BASE_URL = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?'
VALUTE_NAME = "cc"
VALUTE_RATE = 'rate'
DATE = 'exchangedate'
CONVERT, BECK, LEN_COM = 'Convert', 'Beck', 'Len'
VALUTE, SETUP, HIS, INFO = 'Valute', 'Setup', 'Showhistory', 'Info'
LEN_CONV_COMAND, LEN_H_COM = 3, 2
MONTH, SECMONTH, YEAR = 30, 28, 12
DEFAULT_STRING, ZERO, ZERO_LIST = '', 0, []
CHECK_RESULT = [1, 2, False]
INTERNET_ERROR_MASSAGE = 'No internet connection'


def redactdate(date_d, date_m, date_y):
    '''
    :param date_d: int
    :param date_m: int
    :param date_y: int
    :return: str
    '''

    if date_m > 9 and date_d > 9:
        rez = f'{date_y}{date_m}{date_d}'
    elif date_d > 9 and date_m < 10:
        rez = f'{date_y}0{date_m}{date_d}'
    elif date_d < 10 and date_m > 9:
        rez = f'{date_y}{date_m}0{date_d}'
    else:
        rez = f'{date_y}0{date_m}0{date_d}'
    return rez


def set_valute(set_val):
    '''
    :param set_val: int
    :return: None
    '''
    DEFAULT_VALCODE = set_val
    return 'DEFAULT_VALCODE changed'


def set_len(set_len_h):
    '''
    :param set_len_h: int
    :return: None
    '''
    DEFAULT_HISTORY_LEN = int(set_len_h)
    return 'DEFAULT_HISTORY_LEN changed'


def create_value_list():
    '''
    :return: list
    '''
    valutelist = ZERO_LIST
    query = send_request()
    for i in query.json():
        valutelist.append(i[VALUTE_NAME])
    return valutelist


def showmainmenu():
    '''

    :return: str main menu
    '''
    return '----------Main Menu----------\n\
0) Convert [convert, 0, c]\n\
1) Info [info, 1, , i]\n\
2) Showhistory [showhistory, 2, h, history]\n\
3) Setup [setup, 3, s]\n\
4) Exit [exit, 4]'


def showsetupmenu():
    '''
    :return: str setup menu
    '''
    return '------------SETUP------------\n\
0) Set another default valute (command 0 or valute)\n\
1) Set another default history len (command 1 or len)\n\
2) Beck (command 2 or beck)'


def check_convert_args(dec):
    '''
    check args for convert
    :param dec:
    :return:
    '''
    valutes = create_value_list()
    if len(dec) != LEN_CONV_COMAND:
        check = 'Command convert take 2 arguments'
    elif dec[2] not in valutes:
        check = 'Unknown valute at arg2'
    else:
        check = True
    return check


def solo_valute_convert(dec):
    '''
    function used if user import one valutes
    :param dec:
    :return:
    '''
    response = send_request(dec[2])
    if response == INTERNET_ERROR_MASSAGE:
        rezult_of_convert = INTERNET_ERROR_MASSAGE
    else:
        rezult_of_convert = f'{dec[1]} {DEFAULT_VALCODE} = \
                              {float(dec[1])/response.json()[0][VALUTE_RATE]} {dec[2]}'
    return rezult_of_convert


def double_valute_convert(dec):
    '''
    function used if user import two valutes
    :param dec:
    :return:
    '''
    valutes = create_value_list()
    if dec[1].isnumeric():
        number = dec[1]
        valute = DEFAULT_VALCODE
    else:
        up_val = list(dec[1])
        number = DEFAULT_STRING
        valute = DEFAULT_STRING
        for i in up_val:
            if i.isnumeric():
                number = f'{number}{i}'
            else:
                valute = f'{valute}{i}'.upper()
        if valute not in valutes or dec[2] not in valutes:
            rezult_of_convert = f"Unknown valute"
    main_val = send_request(valute).json()[0][VALUTE_RATE]
    sec_val = send_request(dec[2].upper()).json()[0][VALUTE_RATE]
    if INTERNET_ERROR_MASSAGE in (main_val, sec_val):
        rezult_of_convert = INTERNET_ERROR_MASSAGE
    else:
        rezult_of_convert = f'{number} {valute} = {(main_val / sec_val) * int(number)} {dec[2]}'
    return rezult_of_convert


def convert(command):
    '''
    :param command: str
    :return: str
    '''
    dec = command.upper().split()
    if check_convert_args(dec) is not True:
        rezult_of_convert = check_convert_args(dec)

    elif dec[1].isnumeric() and DEFAULT_VALCODE == 'UAH':
        rezult_of_convert = solo_valute_convert(dec)
    else:
        rezult_of_convert = double_valute_convert(dec)
    return rezult_of_convert


def send_request(valute=None, date_for_request=None):
    '''
    function for sanding requests and returning their information
    :param valute str:
    :param date_for_request str:
    :return: str
    '''
    if valute is not None:
        is_valute = f'&valcode={valute}'
    else:
        is_valute = ''
    if date_for_request is not None:
        is_date = f'&date={date_for_request}'
    else:
        is_date = ''
    try:
        rez = requests.get(f'{BASE_URL}json{is_valute}{is_date}')
    except ConnectionError:
        rez = INTERNET_ERROR_MASSAGE
    return rez


def info():
    '''

    :return: tuple(DEFAULT_VALCODE, BASE_URL, list_of_values)
    '''
    query = send_request().json()
    list_of_values = ZERO_LIST
    for i in query:
        list_of_values.append({i[VALUTE_NAME]: i[VALUTE_RATE]})
    return DEFAULT_VALCODE, BASE_URL, list_of_values


def checkhistory(com):
    '''
    :param com: str
    :return: int
    '''
    valutes = create_value_list()
    his = com.upper().split()
    if len(his) is LEN_H_COM and his[1] in valutes:
        rezult = CHECK_RESULT[0]
    elif len(his) is LEN_CONV_COMAND and his[2] in valutes and his[1].isnumeric():
        rezult = CHECK_RESULT[1]
    else:
        rezult = CHECK_RESULT[2]
    return rezult


def showhitory(com):
    '''
    :param com: str command
    :return: str
    '''
    rez = ZERO_LIST
    his = com.upper().split()
    if checkhistory(com) is CHECK_RESULT[0]:
        value_of_len_history = DEFAULT_HISTORY_LEN
        val = his[1]
    elif checkhistory(com) is CHECK_RESULT[1]:
        value_of_len_history = int(his[1])
        val = his[2]
    else:
        return 'command error'
    date_today = date.today()
    date_d, date_m, date_y = date_today.day, date_today.month, date_today.year
    while value_of_len_history > 0:
        date_or = redactdate(date_d, date_m, date_y)
        oneday = send_request(val, date_or).json()[0]
        rez.append((oneday[VALUTE_NAME], oneday[VALUTE_RATE], oneday[DATE]))
        date_d -= 1
        if date_d == 0:
            date_d = MONTH
            date_m -= 1
            if date_m == 2:
                date_d = SECMONTH
        if date_m == 0:
            date_m = YEAR
            date_y -= 1
        value_of_len_history -= 1
    return rez


def setup():
    '''

    :return: some setups
    '''
    print(showsetupmenu())
    setup_comand = input()
    if setup_comand in NAMES_OF_FUNCTIONS[BECK]:
        rezult = 'Beck'
    elif setup_comand.count(' ') is ZERO:
        rezult = 'this command take at less 2 args'
    elif setup_comand.split()[0] in NAMES_OF_FUNCTIONS[VALUTE]:
        rezult = set_valute(setup_comand.split()[1])
    elif setup_comand.split()[0] in NAMES_OF_FUNCTIONS[LEN_COM]:
        rezult = set_len(setup_comand.split()[1])
    else:
        rezult = f'It is no command such {setup_comand}'
    return rezult


def donecommand(command):
    '''

    :param command: str commad
    :return: None
    '''
    if command in NAMES_OF_FUNCTIONS[SETUP]:
        setup()
    elif command in NAMES_OF_FUNCTIONS[INFO]:
        inforez = info()
        print('DEFAULT_VALCODE:', inforez[0], '\nBASE_URL:', inforez[1])
        for i in inforez[2]:
            print(i)
    elif command.split()[0] in NAMES_OF_FUNCTIONS[HIS]:
        for i in showhitory(command):
            print(i)
    elif command.split()[0] in NAMES_OF_FUNCTIONS[CONVERT]:
        print(convert(command))
    else:
        print(f'It is no command such {command}')
