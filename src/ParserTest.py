from Language.Parser import *

def parserTest():
    input = 'execute -path = ../scriptUser.adsj'
    Scanner.lineno = 1
    e = parser.parse(input)
    e[0].exec(parser)

parserTest()