from Language.Parser import *

def parserTest():
    input = 'execute -path = /home/bryan/Documentos/USAC/Archivos/2S2023/Laboratorio/Proyecto1/script.adsj'
    Scanner.lineno = 1
    e = parser.parse(input)
    e[0].exec(parser)

parserTest()