from exch import showmainmenu, donecommand, convert, EXIT
import argparse


parser = argparse.ArgumentParser(description='Cache converter')
parser.add_argument('-v', '--value', type=str, default=None,
                    help='value ar value and valute what program should convert')
parser.add_argument('-e', '--endvalute', type=str, default=None,
                    help='the currency in which the value is converted')
def_arg = parser.parse_args()
conv = convert(f'0 {def_arg.value} {def_arg.endvalute}')

if __name__ == '__main__':
    if def_arg.value != None and def_arg.endvalute != None:
        print(conv)
    else:
        print(showmainmenu())
        c = input().lower()
        while c not in EXIT:
            donecommand(c)
            print(showmainmenu())
            c = input().lower()
