
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'RW_add RW_block RW_bm_block RW_bm_inode RW_cat RW_chgrp RW_chmod RW_chown RW_cont RW_copy RW_delete RW_destino RW_disk RW_edit RW_execute RW_fdisk RW_file RW_fileN RW_find RW_fit RW_fs RW_full RW_grp RW_id RW_inode RW_journaling RW_login RW_logout RW_loss RW_ls RW_mbr RW_mkdir RW_mkdisk RW_mkfile RW_mkfs RW_mkgrp RW_mkusr RW_mount RW_move RW_name RW_pass RW_path RW_pause RW_r RW_recovery RW_remove RW_rename RW_rep RW_rmdisk RW_rmgrp RW_rmusr RW_ruta RW_sb RW_size RW_tree RW_type RW_ugo RW_unit RW_unmount RW_user TK_equ TK_fit TK_id TK_number TK_path TK_type TK_unit commentaryINIT : COMMANDSCOMMANDS : COMMANDS COMMAND\n                | COMMAND COMMAND  : EXECUTE\n                | MKDISK\n                | RMDISK\n                | FDISK\n                | REP\n                | COMMENTARYEXECUTE  : RW_execute RW_path TK_equ TK_path\n                | RW_executeMKDISK   : RW_mkdisk MKDISKPARAMS\n                | RW_mkdiskMKDISKPARAMS : MKDISKPARAMS MKDISKPARAM\n                    | MKDISKPARAMMKDISKPARAM  : RW_size TK_equ TK_number\n                    | RW_path TK_equ TK_path\n                    | RW_fit  TK_equ TK_fit\n                    | RW_unit TK_equ TK_unitRMDISK   : RW_rmdisk RW_path TK_equ TK_path\n                | RW_rmdiskFDISK    : RW_fdisk FDISKPARAMS\n                | RW_fdiskFDISKPARAMS  : FDISKPARAMS FDISKPARAM\n                    | FDISKPARAMFDISKPARAM   : RW_size   TK_equ TK_number\n                    | RW_path   TK_equ TK_path\n                    | RW_name   TK_equ TK_id\n                    | RW_unit   TK_equ TK_unit\n                    | RW_type   TK_equ TK_type\n                    | RW_fit    TK_equ TK_fit\n                    | RW_delete TK_equ RW_full\n                    | RW_add    TK_equ TK_numberREP : RW_repCOMMENTARY : commentary'
    
_lr_action_items = {'RW_execute':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,25,26,36,42,51,52,53,54,55,56,57,58,59,60,61,62,63,64,],[10,10,-3,-4,-5,-6,-7,-8,-9,-11,-13,-21,-23,-34,-35,-2,-12,-15,-22,-25,-14,-24,-10,-16,-17,-18,-19,-20,-26,-27,-28,-29,-30,-31,-32,-33,]),'RW_mkdisk':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,25,26,36,42,51,52,53,54,55,56,57,58,59,60,61,62,63,64,],[11,11,-3,-4,-5,-6,-7,-8,-9,-11,-13,-21,-23,-34,-35,-2,-12,-15,-22,-25,-14,-24,-10,-16,-17,-18,-19,-20,-26,-27,-28,-29,-30,-31,-32,-33,]),'RW_rmdisk':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,25,26,36,42,51,52,53,54,55,56,57,58,59,60,61,62,63,64,],[12,12,-3,-4,-5,-6,-7,-8,-9,-11,-13,-21,-23,-34,-35,-2,-12,-15,-22,-25,-14,-24,-10,-16,-17,-18,-19,-20,-26,-27,-28,-29,-30,-31,-32,-33,]),'RW_fdisk':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,25,26,36,42,51,52,53,54,55,56,57,58,59,60,61,62,63,64,],[13,13,-3,-4,-5,-6,-7,-8,-9,-11,-13,-21,-23,-34,-35,-2,-12,-15,-22,-25,-14,-24,-10,-16,-17,-18,-19,-20,-26,-27,-28,-29,-30,-31,-32,-33,]),'RW_rep':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,25,26,36,42,51,52,53,54,55,56,57,58,59,60,61,62,63,64,],[14,14,-3,-4,-5,-6,-7,-8,-9,-11,-13,-21,-23,-34,-35,-2,-12,-15,-22,-25,-14,-24,-10,-16,-17,-18,-19,-20,-26,-27,-28,-29,-30,-31,-32,-33,]),'commentary':([0,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,25,26,36,42,51,52,53,54,55,56,57,58,59,60,61,62,63,64,],[15,15,-3,-4,-5,-6,-7,-8,-9,-11,-13,-21,-23,-34,-35,-2,-12,-15,-22,-25,-14,-24,-10,-16,-17,-18,-19,-20,-26,-27,-28,-29,-30,-31,-32,-33,]),'$end':([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,18,19,25,26,36,42,51,52,53,54,55,56,57,58,59,60,61,62,63,64,],[0,-1,-3,-4,-5,-6,-7,-8,-9,-11,-13,-21,-23,-34,-35,-2,-12,-15,-22,-25,-14,-24,-10,-16,-17,-18,-19,-20,-26,-27,-28,-29,-30,-31,-32,-33,]),'RW_path':([10,11,12,13,18,19,25,26,36,42,52,53,54,55,57,58,59,60,61,62,63,64,],[17,21,24,28,21,-15,28,-25,-14,-24,-16,-17,-18,-19,-26,-27,-28,-29,-30,-31,-32,-33,]),'RW_size':([11,13,18,19,25,26,36,42,52,53,54,55,57,58,59,60,61,62,63,64,],[20,27,20,-15,27,-25,-14,-24,-16,-17,-18,-19,-26,-27,-28,-29,-30,-31,-32,-33,]),'RW_fit':([11,13,18,19,25,26,36,42,52,53,54,55,57,58,59,60,61,62,63,64,],[22,32,22,-15,32,-25,-14,-24,-16,-17,-18,-19,-26,-27,-28,-29,-30,-31,-32,-33,]),'RW_unit':([11,13,18,19,25,26,36,42,52,53,54,55,57,58,59,60,61,62,63,64,],[23,30,23,-15,30,-25,-14,-24,-16,-17,-18,-19,-26,-27,-28,-29,-30,-31,-32,-33,]),'RW_name':([13,25,26,42,57,58,59,60,61,62,63,64,],[29,29,-25,-24,-26,-27,-28,-29,-30,-31,-32,-33,]),'RW_type':([13,25,26,42,57,58,59,60,61,62,63,64,],[31,31,-25,-24,-26,-27,-28,-29,-30,-31,-32,-33,]),'RW_delete':([13,25,26,42,57,58,59,60,61,62,63,64,],[33,33,-25,-24,-26,-27,-28,-29,-30,-31,-32,-33,]),'RW_add':([13,25,26,42,57,58,59,60,61,62,63,64,],[34,34,-25,-24,-26,-27,-28,-29,-30,-31,-32,-33,]),'TK_equ':([17,20,21,22,23,24,27,28,29,30,31,32,33,34,],[35,37,38,39,40,41,43,44,45,46,47,48,49,50,]),'TK_path':([35,38,41,44,],[51,53,56,58,]),'TK_number':([37,43,50,],[52,57,64,]),'TK_fit':([39,48,],[54,62,]),'TK_unit':([40,46,],[55,60,]),'TK_id':([45,],[59,]),'TK_type':([47,],[61,]),'RW_full':([49,],[63,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'INIT':([0,],[1,]),'COMMANDS':([0,],[2,]),'COMMAND':([0,2,],[3,16,]),'EXECUTE':([0,2,],[4,4,]),'MKDISK':([0,2,],[5,5,]),'RMDISK':([0,2,],[6,6,]),'FDISK':([0,2,],[7,7,]),'REP':([0,2,],[8,8,]),'COMMENTARY':([0,2,],[9,9,]),'MKDISKPARAMS':([11,],[18,]),'MKDISKPARAM':([11,18,],[19,36,]),'FDISKPARAMS':([13,],[25,]),'FDISKPARAM':([13,25,],[26,42,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> INIT","S'",1,None,None,None),
  ('INIT -> COMMANDS','INIT',1,'p_INIT','Parser.py',11),
  ('COMMANDS -> COMMANDS COMMAND','COMMANDS',2,'p_COMMANDS','Parser.py',15),
  ('COMMANDS -> COMMAND','COMMANDS',1,'p_COMMANDS','Parser.py',16),
  ('COMMAND -> EXECUTE','COMMAND',1,'p_COMMAND','Parser.py',24),
  ('COMMAND -> MKDISK','COMMAND',1,'p_COMMAND','Parser.py',25),
  ('COMMAND -> RMDISK','COMMAND',1,'p_COMMAND','Parser.py',26),
  ('COMMAND -> FDISK','COMMAND',1,'p_COMMAND','Parser.py',27),
  ('COMMAND -> REP','COMMAND',1,'p_COMMAND','Parser.py',28),
  ('COMMAND -> COMMENTARY','COMMAND',1,'p_COMMAND','Parser.py',29),
  ('EXECUTE -> RW_execute RW_path TK_equ TK_path','EXECUTE',4,'p_EXECUTE','Parser.py',33),
  ('EXECUTE -> RW_execute','EXECUTE',1,'p_EXECUTE','Parser.py',34),
  ('MKDISK -> RW_mkdisk MKDISKPARAMS','MKDISK',2,'p_MKDISK','Parser.py',41),
  ('MKDISK -> RW_mkdisk','MKDISK',1,'p_MKDISK','Parser.py',42),
  ('MKDISKPARAMS -> MKDISKPARAMS MKDISKPARAM','MKDISKPARAMS',2,'p_MKDISKPARAMS','Parser.py',53),
  ('MKDISKPARAMS -> MKDISKPARAM','MKDISKPARAMS',1,'p_MKDISKPARAMS','Parser.py',54),
  ('MKDISKPARAM -> RW_size TK_equ TK_number','MKDISKPARAM',3,'p_MKDISKPARAM','Parser.py',62),
  ('MKDISKPARAM -> RW_path TK_equ TK_path','MKDISKPARAM',3,'p_MKDISKPARAM','Parser.py',63),
  ('MKDISKPARAM -> RW_fit TK_equ TK_fit','MKDISKPARAM',3,'p_MKDISKPARAM','Parser.py',64),
  ('MKDISKPARAM -> RW_unit TK_equ TK_unit','MKDISKPARAM',3,'p_MKDISKPARAM','Parser.py',65),
  ('RMDISK -> RW_rmdisk RW_path TK_equ TK_path','RMDISK',4,'p_RMDISK','Parser.py',69),
  ('RMDISK -> RW_rmdisk','RMDISK',1,'p_RMDISK','Parser.py',70),
  ('FDISK -> RW_fdisk FDISKPARAMS','FDISK',2,'p_FDISK','Parser.py',79),
  ('FDISK -> RW_fdisk','FDISK',1,'p_FDISK','Parser.py',80),
  ('FDISKPARAMS -> FDISKPARAMS FDISKPARAM','FDISKPARAMS',2,'p_FDISKPARAMS','Parser.py',91),
  ('FDISKPARAMS -> FDISKPARAM','FDISKPARAMS',1,'p_FDISKPARAMS','Parser.py',92),
  ('FDISKPARAM -> RW_size TK_equ TK_number','FDISKPARAM',3,'p_FDISKPARAM','Parser.py',100),
  ('FDISKPARAM -> RW_path TK_equ TK_path','FDISKPARAM',3,'p_FDISKPARAM','Parser.py',101),
  ('FDISKPARAM -> RW_name TK_equ TK_id','FDISKPARAM',3,'p_FDISKPARAM','Parser.py',102),
  ('FDISKPARAM -> RW_unit TK_equ TK_unit','FDISKPARAM',3,'p_FDISKPARAM','Parser.py',103),
  ('FDISKPARAM -> RW_type TK_equ TK_type','FDISKPARAM',3,'p_FDISKPARAM','Parser.py',104),
  ('FDISKPARAM -> RW_fit TK_equ TK_fit','FDISKPARAM',3,'p_FDISKPARAM','Parser.py',105),
  ('FDISKPARAM -> RW_delete TK_equ RW_full','FDISKPARAM',3,'p_FDISKPARAM','Parser.py',106),
  ('FDISKPARAM -> RW_add TK_equ TK_number','FDISKPARAM',3,'p_FDISKPARAM','Parser.py',107),
  ('REP -> RW_rep','REP',1,'p_REP','Parser.py',111),
  ('COMMENTARY -> commentary','COMMENTARY',1,'p_COMMENTARY','Parser.py',116),
]
