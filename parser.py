import uuid

import ply.yacc as yacc

from lex import tokens
import AST

vars = {}


def p_programme_statement(p):
    ''' programme : statement '''
    p[0] = AST.ProgramNode(p[1])


def p_programme_recursive(p):
    ''' programme : statement programme '''
    p[0] = AST.ProgramNode([p[1]] + p[2].children)


def p_statement(p):
    ''' statement : assignation
        | structure
        | condition
        | css
        | keyframes
        | animation
        | frame '''
    p[0] = p[1]


def p_statement_print(p):
    ''' statement : LOG expression '''
    p[0] = AST.PrintNode(p[2])


def p_condition(p):
    ''' condition : IF expression '{' programme '}' '''
    p[0] = AST.ConditionNode([p[2], p[4]])


def p_structure(p):
    ''' structure : FOR NUMBER TO NUMBER BY NUMBER '{' programme '}' '''
    p[0] = AST.WhileNode([
        AST.AssignNode([AST.TokenNode("a1"), AST.TokenNode(p[2])]),
        AST.AssignNode([AST.TokenNode("a2"), AST.TokenNode(p[4])]),
        AST.AssignNode([AST.TokenNode("a3"), AST.TokenNode(p[6])]),
        p[8]
    ])


def p_css(p):
    '''css : '@' STRING'''
    p[0] = AST.CssNode(AST.TokenNode(p[2]))



def p_keyframes(p):
    '''keyframes : KEYFRAMES '(' STRING ')' '{' programme '}' '''
    p[0] = AST.KeyframesNode([AST.AssignNode([AST.TokenNode("name"), AST.TokenNode(p[3])]), p[6]])


def p_animation(p):
    '''animation : ANIMATION '(' STRING ',' STRING ')' '{' programme '}' '''
    p[0] = AST.AnimationNode([
        AST.AssignNode([AST.TokenNode("animation_name"), AST.TokenNode(p[3])]),
        AST.AssignNode([AST.TokenNode("selector"), AST.TokenNode(p[5])]),
        p[8]
    ])


def p_frame(p):
    '''frame : FRAME '(' NUMBER ')' '{' programme '}' '''
    p[0] = AST.FrameNode([AST.AssignNode([AST.TokenNode("value"), AST.TokenNode(p[3])]), p[6]])


def p_expression_op(p):
    '''expression : expression ADD_OP expression
            | expression MUL_OP expression'''
    p[0] = AST.OpNode(p[2], [p[1], p[3]])


def p_expression_logic(p):
    ''' expression : expression IS expression '''
    p[0] = AST.IsEqualNode([p[1], p[3]])


def p_expression_num_or_var(p):
    '''expression : NUMBER
        | IDENTIFIER
        | STRING '''
    p[0] = AST.TokenNode(p[1])


def p_expression_paren(p):
    '''expression : '(' expression ')' '''
    p[0] = p[2]

"""
def p_function(p):
    '''expression : IDENTIFIER '(' ')' '{' programme '}' '''
    p[0] = AST.FuncNode([p[1], p[5]])
"""


def p_minus(p):
    ''' expression : ADD_OP expression %prec UMINUS'''
    p[0] = AST.OpNode(p[1], [p[2]])


def p_assign(p):
    ''' assignation : IDENTIFIER ':' expression '''
    p[0] = AST.AssignNode([AST.TokenNode(p[1]), p[3]])


def p_error(p):
    if p:
        print ("Syntax error in line %d" % p.lineno)
        yacc.errok()
    else:
        print ("Sytax error: unexpected end of file!")


precedence = (
    ('left', 'ADD_OP'),
    ('left', 'MUL_OP'),
    ('right', 'UMINUS'),
)


def parse(program):
    return yacc.parse(program)


yacc.yacc(outputdir='generated')

if __name__ == "__main__":
    import sys

    prog = open(sys.argv[1]).read()

    result = yacc.parse(prog, debug=1)

    if result:
        print (result)

        import os

        graph = result.makegraphicaltree()
        name = os.path.splitext(sys.argv[1])[0] + '-ast.pdf'
        graph.write_pdf(name)
        print ("wrote ast to", name)
    else:
        print ("Parsing returned no result!")
