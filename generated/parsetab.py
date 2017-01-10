
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.8'

_lr_method = 'LALR'

_lr_signature = '266D5634A85AA0093BA43ADFE0B02F60'
    
_lr_action_items = {'MUL_OP':([7,9,10,13,14,20,22,23,29,],[-9,-10,16,16,-13,-11,-8,16,-12,]),'LOG':([0,12,25,30,],[1,1,1,1,]),'FOR':([0,12,25,30,],[2,2,2,2,]),')':([7,9,13,14,15,20,22,23,29,],[-9,-10,20,-13,21,-11,-8,-7,-12,]),'(':([1,6,8,9,16,17,],[6,6,6,15,6,6,]),'NUMBER':([1,2,6,8,16,17,18,26,],[7,11,7,7,7,7,24,28,]),'BY':([24,],[26,]),'TO':([11,],[18,]),'ADD_OP':([1,6,7,8,9,10,13,14,16,17,20,22,23,29,],[8,8,-9,8,-10,17,17,-13,8,8,-11,-8,-7,-12,]),';':([3,4,7,9,10,14,20,22,23,29,32,],[12,-3,-9,-10,-4,-13,-11,-8,-7,-12,-5,]),'IDENTIFIER':([1,6,8,16,17,],[9,9,9,9,9,]),'}':([3,4,7,9,10,14,19,20,22,23,27,29,31,32,],[-1,-3,-9,-10,-4,-13,-2,-11,-8,-7,29,-12,32,-5,]),'{':([21,28,],[25,30,]),'$end':([3,4,5,7,9,10,14,19,20,22,23,29,32,],[-1,-3,0,-9,-10,-4,-13,-2,-11,-8,-7,-12,-5,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([1,6,8,16,17,],[10,13,14,22,23,]),'structure':([0,12,25,30,],[4,4,4,4,]),'statement':([0,12,25,30,],[3,3,3,3,]),'programme':([0,12,25,30,],[5,19,27,31,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> programme","S'",1,None,None,None),
  ('programme -> statement','programme',1,'p_programme_statement','parser.py',10),
  ('programme -> statement ; programme','programme',3,'p_programme_recursive','parser.py',15),
  ('statement -> structure','statement',1,'p_statement','parser.py',20),
  ('statement -> LOG expression','statement',2,'p_statement_print','parser.py',25),
  ('structure -> FOR NUMBER TO NUMBER BY NUMBER { programme }','structure',9,'p_structure','parser.py',30),
  ('css -> @ STRING','css',2,'p_css','parser.py',40),
  ('expression -> expression ADD_OP expression','expression',3,'p_expression_op','parser.py',45),
  ('expression -> expression MUL_OP expression','expression',3,'p_expression_op','parser.py',46),
  ('expression -> NUMBER','expression',1,'p_expression_num_or_var','parser.py',51),
  ('expression -> IDENTIFIER','expression',1,'p_expression_num_or_var','parser.py',52),
  ('expression -> ( expression )','expression',3,'p_expression_paren','parser.py',57),
  ('expression -> IDENTIFIER ( ) { programme }','expression',6,'p_function','parser.py',62),
  ('expression -> ADD_OP expression','expression',2,'p_minus','parser.py',68),
  ('assignation -> IDENTIFIER : expression','assignation',3,'p_assign','parser.py',73),
]
