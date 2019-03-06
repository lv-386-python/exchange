'''
main file of valute converter
'''
import argparse
from exch import showmainmenu, donecommand, convert, EXIT


PARSER = argparse.ArgumentParser(description='Cache converter')
PARSER.add_argument('-v', '--value', type=str, default=None,
                    help='value ar value and valute what program should convert')
PARSER.add_argument('-e', '--endvalute', type=str, default=None,
                    help='the currency in which the value is converted')
DEF_ARG = PARSER.parse_args()
CONV = convert(f'0 {DEF_ARG.value} {DEF_ARG.endvalute}')

if __name__ == '__main__':
    if DEF_ARG.value is not None and DEF_ARG.endvalute is not None:
        print(CONV)
    else:
        print(showmainmenu())
        C = input().lower()
        while C not in EXIT:
            donecommand(C)
            print(showmainmenu())
            C = input().lower()
