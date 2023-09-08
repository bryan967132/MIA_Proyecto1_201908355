from Commands.Commentary import Commentary
from Commands.Execute import Execute
from Commands.Mkdisk import Mkdisk
from Commands.Rmdisk import Rmdisk
from Commands.Fdisk import Fdisk
from Commands.Rep import Rep

precedence = ()

def p_INIT(t):
    'INIT : COMMANDS'
    t[0] = t[1]

def p_COMMANDS(t):
    '''COMMANDS : COMMANDS COMMAND
                | COMMAND '''
    if len(t) != 2:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_COMMAND(t):
    '''COMMAND  : EXECUTE
                | MKDISK
                | RMDISK
                | FDISK
                | REP
                | COMMENTARY'''
    t[0] = t[1]

def p_EXECUTE(t):
    '''EXECUTE  : RW_execute RW_path TK_equ TK_path
                | RW_execute'''
    if len(t) != 2:
        t[0] = Execute(t[4])
    else:
        t[0] = Execute()

def p_MKDISK(t):
    '''MKDISK   : RW_mkdisk MKDISKPARAMS
                | RW_mkdisk'''
    if len(t) != 2:
        t[0] = Mkdisk(t.lineno(1), t.lexpos(1))
        t[0].setParams(t[2])
        t[0].exec()
    else:
        t[0] = Mkdisk(t.lineno(1), t.lexpos(1))
        t[0].setParams({})
        t[0].exec()

def p_MKDISKPARAMS(t):
    '''MKDISKPARAMS : MKDISKPARAMS MKDISKPARAM
                    | MKDISKPARAM'''
    if len(t) != 2:
        t[1][t[2][0]] = t[2][1]
        t[0] = t[1]
    else:
        t[0] = {'unit': 'M', 'fit': 'FF', t[1][0]: t[1][1]}

def p_MKDISKPARAM(t):
    '''MKDISKPARAM  : RW_size TK_equ TK_number
                    | RW_path TK_equ TK_path
                    | RW_fit  TK_equ TK_fit
                    | RW_unit TK_equ TK_unit'''
    t[0] = [t[1][1:].lower(), t[3]]

def p_RMDISK(t):
    '''RMDISK   : RW_rmdisk RW_path TK_equ TK_path
                | RW_rmdisk'''
    if len(t) != 2:
        t[0] = Rmdisk(t.lineno(1), t.lexpos(1), t[4])
        t[0].exec()
    else:
        t[0] = Rmdisk(t.lineno(1), t.lexpos(1), )
        t[0].exec()

def p_FDISK(t):
    '''FDISK    : RW_fdisk FDISKPARAMS
                | RW_fdisk'''
    if len(t) != 2:
        t[0] = Fdisk(t.lineno(1), t.lexpos(1))
        t[0].setParams(t[2])
        t[0].exec()
    else:
        t[0] = Fdisk(t.lineno(1), t.lexpos(1))
        t[0].setParams({})
        t[0].exec()

def p_FDISKPARAMS(t):
    '''FDISKPARAMS  : FDISKPARAMS FDISKPARAM
                    | FDISKPARAM'''
    if len(t) != 2:
        t[1][t[2][0]] = t[2][1]
        t[0] = t[1]
    else:
        t[0] = {'unit': 'M', 'fit': 'FF', 'type': 'P', t[1][0]: t[1][1]}

def p_FDISKPARAM(t):
    '''FDISKPARAM   : RW_size   TK_equ TK_number
                    | RW_path   TK_equ TK_path
                    | RW_name   TK_equ TK_id
                    | RW_unit   TK_equ TK_unit
                    | RW_type   TK_equ TK_type
                    | RW_fit    TK_equ TK_fit
                    | RW_delete TK_equ RW_full
                    | RW_add    TK_equ TK_number'''
    t[0] = [t[1][1:].lower(), t[3]]

def p_REP(t):
    '''REP  : RW_rep REPPARAMS
            | RW_rep'''
    if len(t) != 2:
        t[0] = Rep(t.lineno(1), t.lexpos(1))
        t[0].setParams(t[2])
        t[0].exec()
    else:
        t[0] = Rep(t.lineno(1), t.lexpos(1))
        t[0].setParams({})
        t[0].exec()

def p_REPPARAMS(t):
    '''REPPARAMS    : REPPARAMS REPPARAM
                    | REPPARAM'''
    if len(t) != 2:
        t[1][t[2][0]] = t[2][1]
        t[0] = t[1]
    else:
        t[0] = {t[1][0]: t[1][1]}

def p_REPPARAM(t):
    '''REPPARAM : RW_name TK_equ NAME
                | RW_path TK_equ TK_path
                | RW_id   TK_equ TK_id
                | RW_ruta TK_equ TK_path'''
    t[0] = [t[1][1:].lower(), t[3]]

def p_NAME(t):
    '''NAME : RW_mbr
            | RW_disk
            | RW_inode
            | RW_journaling
            | RW_block
            | RW_bm_inode
            | RW_bm_block
            | RW_tree
            | RW_sb
            | RW_file
            | RW_ls'''
    t[0] = t[1]

def p_COMMENTARY(t):
    '''COMMENTARY : commentary'''
    t[0] = Commentary(t[1])
    t[0].exec()

class Sym:
    def __init__(self, type, lexeme, line, pos):
        self.type = type
        self.lexeme = lexeme
        self.line = line
        self.pos = pos

    def getSym(tok):
        attribsTok = str(tok)
        for s in ['LexToken', '(', ')', '\'',]:
            attribsTok = attribsTok.replace(s, '')
        attribsTok = attribsTok.split(',')
        return Sym(attribsTok[0], attribsTok[1], attribsTok[2], attribsTok[3])

def p_error(t):
    t = Sym.getSym(t)
    print(f"Error de sintaxis: {t.type} = {t.lexeme}, línea {t.line}")

from Language.Scanner import *
import ply.yacc as Parser
parser = Parser.yacc()