from Language.Parser import *
import os

def menu():
    os.system('clear')
    print()
    print('Proyecto 1')
    while True:
        execute = input('Command$ ')
        if execute.lower() == 'exit':
            break
        scanner.lineno = 1
        exec = parser.parse(execute)
        if type(exec[0]) == Execute:
            exec[0].exec(parser)

menu()