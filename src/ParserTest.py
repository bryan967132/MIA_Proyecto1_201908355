from Language.Parser import *
import os

def parserTest():
    os.system('clear')
    input = 'execute -path = ../scriptGrp.adsj'
    Scanner.lineno = 1
    e = parser.parse(input)
    e[0].exec(parser)

parserTest()