import re

errors = []

reserveds = {
    'mkdisk'  : 'RW_mkdisk',
    'rmdisk'  : 'RW_rmdisk',
    'fdisk'   : 'RW_fdisk',
    'mount'   : 'RW_mount',
    'unmount' : 'RW_unmount',
    'mkfs'    : 'RW_mkfs',
    'login'   : 'RW_login',
    'logout'  : 'RW_logout',
    'mkgrp'   : 'RW_mkgrp',
    'rmgrp'   : 'RW_rmgrp',
    'mkusr'   : 'RW_mkusr',
    'rmusr'   : 'RW_rmusr',
    'mkfile'  : 'RW_mkfile',
    'cat'     : 'RW_cat',
    'remove'  : 'RW_remove',
    'edit'    : 'RW_edit',
    'rename'  : 'RW_rename',
    'mkdir'   : 'RW_mkdir',
    'copy'    : 'RW_copy',
    'move'    : 'RW_move',
    'find'    : 'RW_find',
    'chown'   : 'RW_chown',
    'chgrp'   : 'RW_chgrp',
    'chmod'   : 'RW_chmod',
    'pause'   : 'RW_pause',
    'recovery': 'RW_recovery',
    'loss'    : 'RW_loss',
    'execute' : 'RW_execute',
    'rep'     : 'RW_rep',
    'b'       : 'TK_unit',
    'k'       : 'TK_unit',
    'm'       : 'TK_unit'
}

tokens = (
    'RW_mkdisk',
    'RW_rmdisk',
    'RW_fdisk',
    'RW_mount',
    'RW_unmount',
    'RW_mkfs',
    'RW_login',
    'RW_logout',
    'RW_mkgrp',
    'RW_rmgrp',
    'RW_mkusr',
    'RW_rmusr',
    'RW_mkfile',
    'RW_cat',
    'RW_remove',
    'RW_edit',
    'RW_rename',
    'RW_mkdir',
    'RW_copy',
    'RW_move',
    'RW_find',
    'RW_chown',
    'RW_chgrp',
    'RW_chmod',
    'RW_pause',
    'RW_recovery',
    'RW_loss',
    'RW_execute',
    'RW_rep',
    'RW_size',
    'RW_path',
    'RW_fit',
    'RW_unit',
    'RW_name',
    'RW_type',
    'RW_delete',
    'RW_add',
    'RW_id',
    'RW_fs',
    'RW_user',
    'RW_pass',
    'RW_grp',
    'RW_r',
    'RW_cont',
    'RW_fileN',
    'RW_destino',
    'RW_ugo',
    'RW_ruta',
    'TK_unit',
    'TK_number',
    'TK_path',
    'TK_id',
    'TK_equ',
    'commentary',
)

m = {
    'EXT': r'[a-zA-Z0-9]+',
    'ID1': r'[a-zA-Z0-9_]+',
    'ID2': r'[a-zA-Z0-9_][a-zA-Z0-9_\s]*',
}

t_RW_mkdisk   = r'(M|m)(K|k)(D|d)(I|i)(S|s)(K|k)'
t_RW_rmdisk   = r'(R|r)(M|m)(D|d)(I|i)(S|s)(K|k)'
t_RW_fdisk    = r'(F|f)(D|d)(I|i)(S|s)(K|k)'
t_RW_mount    = r'(M|m)(O|o)(U|u)(N|n)(T|t)'
t_RW_unmount  = r'(U|u)(N|n)(M|m)(O|o)(U|u)(N|n)(T|t)'
t_RW_mkfs     = r'(M|m)(K|k)(F|f)(S|s)'
t_RW_login    = r'(L|l)(O|o)(G|g)(I|i)(N|n)'
t_RW_logout   = r'(L|l)(O|o)(G|g)(O|o)(U|u)(T|t)'
t_RW_mkgrp    = r'(M|m)(K|k)(G|g)(R|r)(P|p)'
t_RW_rmgrp    = r'(R|r)(M|m)(G|g)(R|r)(P|p)'
t_RW_mkusr    = r'(M|m)(K|k)(U|u)(S|s)(R|r)'
t_RW_rmusr    = r'(R|r)(M|m)(U|u)(S|s)(R|r)'
t_RW_mkfile   = r'(M|m)(K|k)(F|f)(I|i)(L|l)(E|e)'
t_RW_cat      = r'(C|c)(A|a)(T|t)'
t_RW_remove   = r'(R|r)(E|e)(M|m)(O|o)(V|v)(E|e)'
t_RW_edit     = r'(E|e)(D|d)(I|i)(T|t)'
t_RW_rename   = r'(R|r)(E|e)(N|n)(A|a)(M|m)(E|e)'
t_RW_mkdir    = r'(M|m)(K|k)(D|d)(I|i)(R|r)'
t_RW_copy     = r'(C|c)(O|o)(P|p)(Y|y)'
t_RW_move     = r'(M|m)(O|o)(V|v)(E|e)'
t_RW_find     = r'(F|f)(I|i)(N|n)(D|d)'
t_RW_chown    = r'(C|c)(H|h)(O|o)(W|w)(N|n)'
t_RW_chgrp    = r'(C|c)(H|h)(G|g)(R|r)(P|p)'
t_RW_chmod    = r'(C|c)(H|h)(M|m)(O|o)(D|d)'
t_RW_pause    = r'(P|p)(A|a)(U|u)(S|s)(E|e)'
t_RW_recovery = r'(R|r)(E|e)(C|c)(O|o)(V|v)(E|e)(R|r)(Y|y)'
t_RW_loss     = r'(L|l)(O|o)(S|s)(S|s)'
t_RW_execute  = r'(E|e)(X|x)(E|e)(C|c)(U|u)(T|t)(E|e)'
t_RW_rep      = r'(R|r)(E|e)(P|p)'
t_RW_size     = r'\-\s*(S|s)(I|i)(Z|z)(E|e)'
t_RW_path     = r'\-\s*(P|p)(A|a)(T|t)(H|h)'
t_RW_fit      = r'\-\s*(F|f)(I|i)(T|t)'
t_RW_unit     = r'\-\s*(U|u)(N|n)(I|i)(T|t)'
t_RW_name     = r'\-\s*(N|n)(A|a)(M|m)(E|e)'
t_RW_type     = r'\-\s*(T|t)(Y|y)(P|p)(E|e)'
t_RW_delete   = r'\-\s*(D|d)(E|e)(L|l)(E|e)(T|t)(E|e)'
t_RW_add      = r'\-\s*(A|a)(D|d)(D|d)'
t_RW_id       = r'\-\s*(I|i)(D|d)'
t_RW_fs       = r'\-\s*(F|f)(S|s)'
t_RW_user     = r'\-\s*(U|u)(S|s)(E|e)(R|r)'
t_RW_pass     = r'\-\s*(P|p)(A|a)(S|s)(S|s)'
t_RW_grp      = r'\-\s*(G|g)(R|r)(P|p)'
t_RW_r        = r'\-\s*(R|r)'
t_RW_cont     = r'\-\s*(C|c)(O|o)(N|n)(T|t)'
t_RW_fileN    = r'\-\s*(F|f)(I|i)(L|l)(E|e)(N|n)'
t_RW_destino  = r'\-\s*(D|d)(E|e)(S|s)(T|t)(I|i)(N|n)(O|o)'
t_RW_ugo      = r'\-\s*(U|u)(G|g)(O|o)'
t_RW_ruta     = r'\-\s*(R|r)(U|u)(T|t)(A|a)'
t_TK_unit     = r'B|K|M|b|k|m'
t_TK_number   = r'[0-9]+'
t_TK_path     = rf'(((\.\.|\.)?\/)*{m["ID1"]})+(\.{m["EXT"]})|\"(((\.\.|\.)?\/)*{m["ID2"]})+(\.{m["EXT"]})\"'
t_TK_equ      = r'\='

def t_TK_id(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserveds.get(t.value.lower(), 'TK_id') 
    return t

def t_commentary(t):
    r'\#[^\r\n]*'
    t.value = re.sub(r'\#[ ]*', '', t.value)
    t.lexer.lineno += 1
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

def t_error(t):
    errors.append(t.value[0])
    print(f'Caracter no reconocido: {t.value[0]} en la linea {t.lexer.lineno}')
    t.lexer.skip(1)

def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1

import ply.lex as Scanner
scanner = Scanner.lex()