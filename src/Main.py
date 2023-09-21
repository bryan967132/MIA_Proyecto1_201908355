from Language.Parser import *
import os

def menu():
    os.system('clear')
    print()
    print('\n\033[34m Proyecto 1\033[0m')
    while True:
        try:
            execute = input(f'\033[34m Command$ \033[0m')
            if execute.lower() == 'exit':
                break
            scanner.lineno = 1
            exec = parser.parse(execute)
            if type(exec[0]) == Execute:
                exec[0].exec(parser)
        except:
            pass
        print()

menu()