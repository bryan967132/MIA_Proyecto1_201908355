from Language.Parser import *

def menu():
    print()
    print('Proyecto 1')
    while True:
        execute = input('Command$ ')
        if execute.lower() == 'exit':
            break
        Scanner.lineno = 1
        exec = parser.parse(execute)
        exec[0].exec(parser)

menu()