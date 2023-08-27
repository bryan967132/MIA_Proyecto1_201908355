from Language.Scanner import *
import re

def scannerTest():
    input = open('../script.adsj').read()
    scanner.input(input)
    while True:
        token = scanner.token()
        if not token:
            break
        print(
            '{:<12}{:<30}{:<5}{:<5}'
            .format(
                token.type,
                token.value,
                token.lineno,
                token.lexpos
            )
        )
    print()

scannerTest()