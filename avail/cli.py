import sys
import colorama
from .checker import ALL_CHECKERS


def main(argv):
    colorama.init()
    last_category = None
    exit_code = 0

    for checker in sorted(ALL_CHECKERS, key=lambda x: (x.category, x.name)):
        if last_category != checker.category:
            print(colorama.Fore.LIGHTWHITE_EX + checker.category)
            last_category = checker.category
        try:
            available = checker.check_availability(argv[0])
            if available:
                color = colorama.Fore.LIGHTGREEN_EX
                symbol = 'Y'
            else:
                color = colorama.Fore.LIGHTRED_EX
                symbol = 'N'
        except Exception:
            color = colorama.Fore.LIGHTYELLOW_EX
            exit_code = 1
            symbol = '?'

        sys.stdout.write(colorama.Fore.LIGHTWHITE_EX + ' - ' + 
                         color + '[%s] ' % symbol +
                         checker.name + '\n' + colorama.Style.RESET_ALL)

    return exit_code
