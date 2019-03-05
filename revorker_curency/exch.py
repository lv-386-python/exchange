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
LEN_CONV_COMAND = 3
MONTH, SECMONTH, YEAR = 30, 28, 12
DEFAULT_STRING = ''
CHECK_RESULT = [1, 2, False]


def redactdate(date_d, date_m, date_y):
    '''
    :param dd: int
    :param dm: int
    :param dy: int
    :return: str
    '''

    if date_m > 9 and date_d > 9:
        return f'{date_y}{date_m}{date_d}'
    elif date_d > 9 and date_m < 10:
        return f'{date_y}0{date_m}{date_d}'
    elif date_d < 10 and date_m > 9:
        return f'{date_y}{date_m}0{date_d}'
    else:
        return f'{date_y}0{date_m}0{date_d}'


def set_valute(set_val):
    '''
    :param set_val: int
    :return: None
    '''
    DEFAULT_VALCODE = set_val


def set_len(set_len_h):
    '''
    :param set_len_h: int
    :return: None
    '''
    DEFAULT_HISTORY_LEN = int(set_len_h)


def create_value_list():
    '''
    :return: list
    '''
    valutelist = []
    q = requests.get(f'{BASE_URL}&json')
    for i in q.json():
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


def convert(command):
    '''
    :param command: str
    :return: str
    '''
    valutes = create_value_list()
    dec = command.upper().split()
    if len(dec) != LEN_CONV_COMAND:
        return 'Command convert take 2 arguments'
    elif dec[2] not in valutes:
        return 'Unknown valute at arg2'
    elif dec[1].isnumeric() and DEFAULT_VALCODE == 'UAH':
        response = requests.get(f'{BASE_URL}valcode={dec[2]}&json')
        return f'{dec[1]} {DEFAULT_VALCODE} = {float(dec[1])/response.json()[0][VALUTE_RATE]} {dec[2]}'
    else:
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
                return f"Unknown valute"
        main_val = requests.get(f'{BASE_URL}json&valcode={valute}').json()[0][VALUTE_RATE]
        sec_val = requests.get(f'{BASE_URL}json&valcode={dec[2].upper()}').json()[0][VALUTE_RATE]
        return f'{number} {valute} = {(main_val/sec_val)*int(number)} {dec[2]}'


def info():
    '''

    :return: tuple(DEFAULT_VALCODE, BASE_URL, list_of_values)
    '''
    query = requests.get(f'{BASE_URL}json').json()
    list_of_values = []
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
    if len(his) == 2 and his[1] in valutes:
        return CHECK_RESULT[0]
    elif len(his) == 3 and his[2] in valutes and his[1].isnumeric():
        return CHECK_RESULT[1]
    else:
        return CHECK_RESULT[2]


def showhitory(com):
    '''
    :param com: str command
    :return: str
    '''
    rez = []
    his = com.upper().split()
    if checkhistory(com) is CHECK_RESULT[0]:
        v = DEFAULT_HISTORY_LEN
        val = his[1]
    elif checkhistory(com) is CHECK_RESULT[1]:
        v = int(his[1])
        val = his[2]
    else:
        return 'command error'
    date_today = date.today()
    date_d, date_m, date_y = date_today.day, date_today.month, date_today.year
    while v > 0:
        date_or = redactdate(date_d, date_m, date_y)
        oneday = requests.get(f'{BASE_URL}valcode={val}&date={date_or}&json').json()[0]
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
        v -= 1
    return rez


def setup():
    '''

    :return: some setups
    '''
    print(showsetupmenu())
    setup_comand = input()
    if setup_comand in NAMES_OF_FUNCTIONS[BECK]:
        pass
    elif setup_comand.count(' ') is 0:
        return 'this command take at less 2 args'
    elif setup_comand.split()[0] in NAMES_OF_FUNCTIONS[VALUTE]:
        set_valute(setup_comand.split()[1])
    elif setup_comand.split()[0] in NAMES_OF_FUNCTIONS[LEN_COM]:
        set_len(setup_comand.split()[1])
    else:
        return f'It is no command such {setup_comand}'


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
