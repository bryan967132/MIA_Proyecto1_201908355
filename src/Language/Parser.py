from Commands.Commentary import Commentary
from Commands.Execute import Execute
from Commands.Mkdisk import Mkdisk
from Commands.Rmdisk import Rmdisk
from Commands.Fdisk import Fdisk
from Commands.Mount import Mount
from Commands.Unmount import Unmount
from Commands.Mkfs import Mkfs
from Commands.Login import Login
from Commands.Logout import Logout
from Commands.Mkgrp import Mkgrp
from Commands.Rmgrp import Rmgrp
from Commands.Mkusr import Mkusr
from Commands.Rmusr import Rmusr
from Commands.Mkfile import Mkfile
from Commands.Cat import Cat
from Commands.Remove import Remove
from Commands.Edit import Edit
from Commands.Remove import Remove
from Commands.Rename import Rename
from Commands.Mkdir import Mkdir
from Commands.Pause import Pause
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
                | MOUNT
                | UNMOUNT
                | MKFS
                | LOGIN
                | LOGOUT
                | MKGRP
                | RMGRP
                | MKUSR
                | RMUSR
                | MKFILE
                | CAT
                | REMOVE
                | EDIT
                | RENAME
                | MKDIR
                | PAUSE
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
    t[0] = [t[1][1:].lower().strip(), t[3]]

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
    t[0] = [t[1][1:].lower().strip(), t[3]]

def p_MOUNT(t):
    '''MOUNT    : RW_mount MOUNTPARAMS
                | RW_mount'''
    if len(t) != 2:
        t[0] = Mount(t.lineno(1), t.lexpos(1))
        t[0].setParams(t[2])
        t[0].exec()
    else:
        t[0] = Mount(t.lineno(1), t.lexpos(1))
        t[0].setParams({})
        t[0].exec()

def p_MOUNTPARAMS(t):
    '''MOUNTPARAMS  : MOUNTPARAMS MOUNTPARAM
                    | MOUNTPARAM'''
    if len(t) != 2:
        t[1][t[2][0]] = t[2][1]
        t[0] = t[1]
    else:
        t[0] = {t[1][0]: t[1][1]}

def p_MOUNTPARAM(t):
    '''MOUNTPARAM   : RW_path TK_equ TK_path
                    | RW_name TK_equ TK_id'''
    t[0] = [t[1][1:].lower().strip(), t[3]]

def p_UNMOUNT(t):
    '''UNMOUNT  : RW_unmount RW_id TK_equ TK_id
                | RW_unmount'''
    if len(t) != 2:
        t[0] = Unmount(t.lineno(1), t.lexpos(1))
        t[0].setParams({t[2][1:].lower(): t[4]})
        t[0].exec()
    else:
        t[0] = Unmount(t.lineno(1), t.lexpos(1))
        t[0].setParams({})
        t[0].exec()

def p_MKFS(t):
    '''MKFS : RW_mkfs MKFSPARAMS
            | RW_mkfs'''
    if len(t) != 2:
        t[0] = Mkfs(t.lineno(1), t.lexpos(1))
        t[0].setParams(t[2])
        t[0].exec()
    else:
        t[0] = Mkfs(t.lineno(1), t.lexpos(1))
        t[0].setParams({})
        t[0].exec()

def p_MKFSPARAMS(t):
    '''MKFSPARAMS   : MKFSPARAMS MKFSPARAM
                    | MKFSPARAM'''
    if len(t) != 2:
        t[1][t[2][0]] = t[2][1]
        t[0] = t[1]
    else:
        t[0] = {'fs':'2fs', t[1][0]: t[1][1]}

def p_MKFSPARAM(t):
    '''MKFSPARAM    : RW_id   TK_equ TK_id
                    | RW_type TK_equ RW_full
                    | RW_fs   TK_equ RW_2fs
                    | RW_fs   TK_equ RW_3fs'''
    t[0] = [t[1][1:].lower().strip(), t[3]]

def p_LOGIN(t):
    '''LOGIN    : RW_login LOGINPARAMS
                | RW_login'''
    if len(t) != 2:
        t[0] = Login(t.lineno(1), t.lexpos(1))
        t[0].setParams(t[2])
        t[0].exec()
    else:
        t[0] = Login(t.lineno(1), t.lexpos(1))
        t[0].setParams({})
        t[0].exec()

def p_LOGINPARAMS(t):
    '''LOGINPARAMS  : LOGINPARAMS LOGINPARAM
                    | LOGINPARAM'''
    if len(t) != 2:
        t[1][t[2][0]] = t[2][1]
        t[0] = t[1]
    else:
        t[0] = {t[1][0]: t[1][1]}

def p_LOGINPARAM(t):
    '''LOGINPARAM   : RW_user TK_equ TK_id
                    | RW_pass TK_equ TK_id
                    | RW_pass TK_equ TK_number
                    | RW_id   TK_equ TK_id'''
    t[0] = [t[1][1:].lower().strip(), t[3]]

def p_LOGOUT(t):
    '''LOGOUT : RW_logout'''
    t[0] = Logout(t.lineno(1), t.lexpos(1))
    t[0].exec()

def p_MKGRP(t):
    '''MKGRP    : RW_mkgrp RW_name TK_equ TK_id
                | RW_mkgrp'''
    if len(t) != 2:
        t[0] = Mkgrp(t.lineno(1), t.lexpos(1))
        t[0].setParams({t[2][1:].lower().strip(): t[4]})
        t[0].exec()
    else:
        t[0] = Mkgrp(t.lineno(1), t.lexpos(1))
        t[0].setParams({})
        t[0].exec()
    

def p_RMGRP(t):
    '''RMGRP    : RW_rmgrp RW_name TK_equ TK_id
                | RW_rmgrp'''
    if len(t) != 2:
        t[0] = Rmgrp(t.lineno(1), t.lexpos(1))
        t[0].setParams({t[2][1:].lower().strip(): t[4]})
        t[0].exec()
    else:
        t[0] = Rmgrp(t.lineno(1), t.lexpos(1))
        t[0].setParams({})
        t[0].exec()


def p_MKUSR(t):
    '''MKUSR    : RW_mkusr MKUSERPARAMS
                | RW_mkusr'''
    if len(t) != 2:
        t[0] = Mkusr(t.lineno(1), t.lexpos(1))
        t[0].setParams(t[2])
        t[0].exec()
    else:
        t[0] = Mkusr(t.lineno(1), t.lexpos(1))
        t[0].setParams({})
        t[0].exec()

def p_MKUSERPARAMS(t):
    '''MKUSERPARAMS : MKUSERPARAMS MKUSERPARAM
                    | MKUSERPARAM'''
    if len(t) != 2:
        t[1][t[2][0]] = t[2][1]
        t[0] = t[1]
    else:
        t[0] = {t[1][0]: t[1][1]}

def p_MKUSERPARAM(t):
    '''MKUSERPARAM  : RW_user TK_equ TK_id
                    | RW_pass TK_equ TK_id
                    | RW_grp  TK_equ TK_id'''
    t[0] = [t[1][1:].lower().strip(), t[3]]

def p_RMUSR(t):
    '''RMUSR    : RW_rmusr RW_user TK_equ TK_id
                | RW_rmusr'''
    if len(t) != 2:
        t[0] = Rmusr(t.lineno(1), t.lexpos(1))
        t[0].setParams({t[2][1:].lower().strip(): t[4]})
        t[0].exec()
    else:
        t[0] = Rmusr(t.lineno(1), t.lexpos(1))
        t[0].setParams({})
        t[0].exec()

def p_MKFILE(t):
    '''MKFILE   : RW_mkfile MKFILEPARAMS
                | RW_mkfile'''
    if len(t) != 2:
        t[0] = Mkfile(t.lineno(1), t.lexpos(1))
        t[0].setParams(t[2])
        t[0].exec()
    else:
        t[0] = Mkfile(t.lineno(1), t.lexpos(1))
        t[0].setParams({})
        t[0].exec()

def p_MKFILEPARAMS(t):
    '''MKFILEPARAMS : MKFILEPARAMS MKFILEPARAM
                    | MKFILEPARAM'''
    if len(t) != 2:
        t[1][t[2][0]] = t[2][1]
        t[0] = t[1]
    else:
        t[0] = {'r': False, t[1][0]: t[1][1]}

def p_MKFILEPARAM(t):
    '''MKFILEPARAM  : RW_path TK_equ TK_path
                    | RW_size TK_equ TK_number
                    | RW_cont TK_equ TK_path
                    | RW_r'''
    if t[1][1:].lower().strip() == 'r':
        t[0] = ['r', True]
    else:
        t[0] = [t[1][1:].lower().strip(), t[3]]

def p_CAT(t):
    '''CAT  : RW_cat CATFILES
            | RW_cat'''
    if len(t) != 2:
        t[0] = Cat(t.lineno(1), t.lexpos(1))
        t[0].setParams(t[2])
        t[0].exec()
    else:
        t[0] = Cat(t.lineno(1), t.lexpos(1))
        t[0].setParams([])
        t[0].exec()

def p_CATFILES(t):
    '''CATFILES : CATFILES CATFILE
                | CATFILE'''
    if len(t) != 2:
        t[1].append(t[2])
        t[0] = t[1]
    else:
        t[0] = [t[1]]

def p_CATFILE(t):
    '''CATFILE  : RW_fileN TK_equ TK_path'''
    t[0] = [t[1][-1], t[3]]

def p_REMOVE(t):
    '''REMOVE   : RW_remove RW_path TK_equ TK_path
                | RW_remove'''

def p_EDIT(t):
    '''EDIT : RW_edit EDITPARAMS
            | RW_edit'''

def p_EDITPARAMS(t):
    '''EDITPARAMS   : EDITPARAMS EDITPARAM
                    | EDITPARAM'''

def p_EDITPARAM(t):
    '''EDITPARAM    : RW_path TK_equ TK_path
                    | RW_cont TK_equ TK_path'''

def p_RENAME(t):
    '''RENAME   : RW_rename RENAMEPARAMS
                | RW_rename'''

def p_RENAMEPARAMS(t):
    '''RENAMEPARAMS : RENAMEPARAMS RENAMEPARAM
                    | RENAMEPARAM'''

def p_RENAMEPARAM(t):
    '''RENAMEPARAM  : RW_path TK_equ TK_path
                    | RW_name TK_equ TK_id'''

def p_MKDIR(t):
    '''MKDIR    : RW_mkdir MKDIRPARAMS
                | RW_mkdir'''
    if len(t) != 2:
        t[0] = Mkdir(t.lineno(1), t.lexpos(1))
        t[0].setParams(t[2])
        t[0].exec()
    else:
        t[0] = Mkdir(t.lineno(1), t.lexpos(1))
        t[0].setParams({})
        t[0].exec()

def p_MKDIRPARAMS(t):
    '''MKDIRPARAMS  : MKDIRPARAMS MKDIRPARAM
                    | MKDIRPARAM'''
    if len(t) != 2:
        t[1][t[2][0]] = t[2][1]
        t[0] = t[1]
    else:
        t[0] = {'r': False, t[1][0]: t[1][1]}

def p_MKDIRPARAM(t):
    '''MKDIRPARAM   : RW_path TK_equ TK_path
                    | RW_r'''
    if t[1][1:].lower().strip() == 'path':
        t[0] = ['path', t[3]]
    elif t[1][1:].lower().strip() == 'r':
        t[0] = ['r', True]

def p_PAUSE(t):
    '''PAUSE : RW_pause'''
    t[0] = Pause(t.lineno(1), t.lexpos(1))
    t[0].exec()

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
    t[0] = [t[1][1:].lower().strip(), t[3]]

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

def p_error(t):
    print(f"\033[31m -> Error de Sintaxis: {t.type} = {t.value}. [{t.lineno}:{t.lexpos}]\033[0m")

from Language.Scanner import *
import ply.yacc as Parser
parser = Parser.yacc()