from Language.Parser import *
import os

def parserTest():
    os.system('clear')
    # input = 'execute -path = "../Calificacion/Parte 1/1_crear_discos.adsj"'
    # input = 'execute -path = "../Calificacion/Parte 1/2_crear_particiones.adsj"'
    # input = 'execute -path = "../Calificacion/Parte 1/3_montar_particiones.adsj"'
    # input = 'execute -path = "../Calificacion/Parte 1/4_editar_particiones.adsj"'
    # input = 'execute -path = "../Calificacion/Parte 1/5_eliminar_particiones_discos.adsj"'
    # input = 'execute -path = "../Calificacion/Parte 1/6_reportes_parte_1.adsj"'
    # input = 'execute -path = "../Calificacion/Parte 1/parte_1_completa.adsj"'
    # input = 'execute -path = "../Calificacion/Parte 2/inicio_parte_2.adsj"'
    input = 'execute -path = "../Calificacion/Parte 2/parte_2_completa.adsj"'
    Scanner.lineno = 1
    e = parser.parse(input)
    e[0].exec(parser)

parserTest()