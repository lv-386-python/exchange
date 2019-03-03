import requests
from datetime import date


class Menu:
    def __init__(self):
        self.defhistory = 7
        self.param = {}
        self.namesfuct = {'Convert': ['convert', '0', 'c'],
                          'Info': ['info', '1', 'i'],
                          'Showhistory': ['showhistory', '2', 'h', 'history'],
                          'Setup': ['setup', '3', 's']}
        self.param['valcode'] = 'USD'
        self.param['defvalcode'] = 'UAH'
        self.url = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange'
        self.baseurl = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json'
        self.valutelist = []
        q = requests.get(self.baseurl)
        for i in q.json():
            self.valutelist.append(i['cc'])

    def showmainmenu(self):
        pass
        print('----------Main Menu----------')
        print('0) Convert [convert, 0, c]')
        print('1) Info [info, 1, , i]')
        print('2) Showhistory [showhistory, 2, h, history]')
        print('3) Setup [setup, 3, s]')
        print('4) Exit [exit, 4]')

    def showsetupmenu(self):
        print('------------SETUP------------')
        print('0) Set another default valute (command 0 or valute)')
        print('1) Set another default history len (command 1 or len)')
        print('2) Beck (command 2 or beck)')

    def convert(self, command):
        dec = command.upper().split()
        if len(dec) != 3:
            print('Command convert take 2 arguments')
        elif dec[2] not in self.valutelist:
            print('Unknown valute at arg2')
        elif dec[1].isnumeric() and self.param['defvalcode'] == 'UAH':
                valute = 'UAH'
                self.param['valcode'] = dec[2]
                response = requests.get(self.baseurl, params=self.param)
                print(response.json())
                print(dec[1], valute, ' = ', float(dec[1])/response.json()[0]['rate'], dec[2])

        else:
            if dec[1].isnumeric():
                number = dec[1]
                valute = self.param['defvalcode']
            else:
                up = list(dec[1])
                number = ''
                valute = ''
                for i in up:
                    if i.isnumeric():
                        number = f'{number}{i}'
                    else:
                        valute = f'{valute}{i}'
            self.param['valcode'] = valute
            main_val = requests.get(self.baseurl, params=self.param).json()[0]['rate']
            self.param['valcode'] = dec[2]
            sec_val = requests.get(self.baseurl, params=self.param).json()[0]['rate']
            print(number, valute, ' = ', (main_val/sec_val)*int(number), dec[2])

    def info(self):
        print(self.param['defvalcode'])
        print(self.baseurl)
        query = requests.get(self.baseurl).json()
        for i in query:
            print(i['cc'], i['rate'])

    def showhitory(self, com):
        val = ''
        his = com.upper().split()
        if len(his) == 2 and his[1] in self.valutelist:
            v = self.defhistory
            val = his[1]
        elif len(his) == 2 and his[1] not in self.valutelist:
            print('unknown valute')
            return
        elif len(his) == 2:
            print('eror command format')
            return
        elif len(his) == 3 and his[2] not in self.valutelist:
            print('unknown valute')
            return
        elif len(his) == 3 and not his[1].isnumeric():
            print('error history value')
            return
        elif len(his) == 3 and his[2] in self.valutelist and his[1].isnumeric():
            v = int(his[1])
            val = his[2]
        else:
            print('command error')
            return
        dat = date.today()
        dd, dm, dy = dat.day, dat.month, dat.year
        print(val)
        for v in range(self.defhistory):
            if dm > 9 and dd >9:
                date_or = f'{dy}{dm}{dd}'
            elif dd > 9 and dm < 10:
                date_or = f'{dy}0{dm}{dd}'
            elif dd < 10 and dm > 9:
                date_or = f'{dy}{dm}0{dd}'
            else:
                date_or = f'{dy}0{dm}0{dd}'
            oneday = requests.get(f'{self.url}?valcode={val}&date={date_or}&json').json()[0]
            print(oneday['cc'], oneday['rate'], oneday['exchangedate'])
            dd -= 1
            if dd == 0:
                dd = 30
                dm -= 1
                if dm == 2:
                    dd = 28
            if dm == 0:
                dm = 12
                dy -=1

    def set_valute(self, set):
        pass
        self.param['defvalcode'] = set

    def set_len(self, set):
        pass
        self.defhistory = int(set)

    def setup(self):
        pass
        self.showsetupmenu()
        setup_comand = input()
        if setup_comand in ['2', 'beck']:
            pass
        elif setup_comand.count(' ') is 0:
            print('this command take at less 2 args')
        elif setup_comand.split()[0] in ['0', 'valute']:
            self.set_valute(setup_comand.split()[1])
        elif setup_comand.split()[0] in ['1', 'len']:
            self.set_len(setup_comand.split()[1])
        else:
            print(f'It is no command such {setup_comand}')

    def donecommand(self, command):
        if command in self.namesfuct['Setup']:
            self.setup()
        elif command in self.namesfuct['Info']:
            self.info()
        elif command.split()[0] in self.namesfuct['Showhistory']:
            self.showhitory(command)
        elif command.split()[0] in self.namesfuct['Convert']:
            self.convert(command)
        else:
            print(f'It is no command such {command}')


if __name__ == '__main__':
    a = Menu()
    while True:
        a.showmainmenu()
        c = input().lower()
        if c in ['exit', '4']:
            break
        else:
            a.donecommand(c)
    print('------------EXIT-------------')
