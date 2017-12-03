from sys import argv
from interpreter import Interpreter
import pprint
import ox

file_name, lf_source = argv

in_file = open(lf_source)
code = in_file.read()

lexer = ox.make_lexer([
    ('NUMBER', r'\d+'),
    ('NAME', r'[-a-zA-Z]+'),
    ('COMMENT', r';.*'),
    ('NEWLINE', r'\n'),
    ('SPACE', r'\s+'),
    ('RIGHT', r'right'),
    ('LEFT', r'left'),
    ('INC', r'inc'),
    ('DEC', r'dec'),
    ('ADD',r'add'),
    ('SUB',r'sub'),
    ('PRINT', r'print'),
    ('READ', r'read'),
    ('DO',r'do'),
    ('LOOP', r'loop'),
    ('DEF', r'def'),
    ('PARENTHESIS_B', r'\('),
    ('PARENTHESIS_A', r'\)')
])

#Seting tokens
tokens = ['NUMBER','INC', 'DEC','SUB', 'ADD','RIGHT', 'LEFT','PRINT','DO','NAME','LOOP',
            'READ','DEF','PARENTHESIS_A','PARENTHESIS_B']

op = lambda op: (op)
operator = lambda type_op: (type_op)

#making parser
parser = ox.make_parser([
    ('program : PARENTHESIS_B expr PARENTHESIS_A', lambda x,y,z: y),
    ('program : PARENTHESIS_B PARENTHESIS_A', lambda x,y: '()'),
    ('expr : operator expr', lambda x,y: [x,] + y),
    ('expr : operator', lambda x: [x,]),
    ('operator : program', operator),
    ('operator : LOOP', operator),
    ('operator : DO', operator),
    ('operator : RIGHT', operator),
    ('operator : LEFT', operator),
    ('operator : READ', operator),
    ('operator : INC', operator),
    ('operator : DEC', operator),
    ('operator : DEF', operator),
    ('operator : PRINT', operator),
    ('operator : ADD', operator),
    ('operator : SUB', operator),
    ('operator : NAME', operator),
    ('operator : NUMBER', lambda x: float(x)),
], tokens)


pp = pprint.PrettyPrinter(width=60, compact=True)

tokens = lexer(code)
tokens = [token for token in tokens if token.type != 'COMMENT' and token.type != 'SPACE']
ast = parser(tokens)
print(ast)

interpreter = Interpreter(ast)
interpreter.eval(interpreter.command_list)
