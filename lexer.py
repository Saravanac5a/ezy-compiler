import ply.lex as lex
import ply.yacc as yacc

tokens = ['NUM',
          'STR',
          'ID',
          'DLABEL',
          'ARIT',
          'COMP',
          'ASSIGN',
          'COMMA',
          'BEGIN',
          'END',
          'VAR', 
          'SEMICOLON',
          'LPAREN',
          'RPAREN',
          'IN',
          'OUT',
          'INOUT',
          'RETURN',
          'EXIT',
          'READ',
          'PROC',
          'IF',
          'GOTO',
          'PRINT',
          'PRINTLN',
          'CALL']

t_BEGIN = r'begin'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_END = r'end'
t_VAR = r'var'
t_IN = r'in'
t_OUT = r'out'
t_INOUT = r'inout'
t_RETURN = r'return'
t_EXIT = r'exit'
t_IF = r'if'
t_GOTO = r'goto'
t_READ = r'read'
t_PRINTLN = r'println'
t_PRINT = r'print'
t_CALL = r'call'
t_PROC = r'proc'
t_ignore = " \t"
t_ARIT = r'\+|\-|\*|\/'
t_COMP = r'<|>|<=|>=|<>|=='
t_ASSIGN = r'='
t_COMMA = r','

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STR(t):
    r'"[^][^]*"|\'[^][^]*\''
    return t

def t_DLABEL(t):
    r'[a-zA-Z][a-zA-Z0-9_]*:'
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    if t.value == 'begin':
        t.type = 'BEGIN'
    elif t.value == 'end':
        t.type = 'END'
    elif t.value == 'proc':
        t.type = 'PROC'
    elif t.value == 'var':
        t.type = 'VAR'
    elif t.value == 'inout':
        t.type = 'INOUT'
    elif t.value == 'in':
        t.type = 'IN'
    elif t.value == 'out':
        t.type = 'OUT'
    elif t.value == 'return':
        t.type = 'RETURN'
    elif t.value == 'exit':
        t.type = 'EXIT'
    elif t.value == 'println':
        t.type = 'PRINTLN'
    elif t.value == 'print':
        t.type = 'PRINT'
    elif t.value == 'read':
        t.type = 'READ'
    elif t.value == 'goto':
        t.type = 'GOTO'
    elif t.value == 'call':
        t.type = 'CALL'
    elif t.value == 'if':
        t.type = 'IF'
    return t

def t_error(t):
    print("Invalid character: "+str(t)[16]+'\nPlease check and try again')
    t.lexer.skip(1)


lexer = lex.lex()

def p_prog(p):
    '''
    prog : vardecls procdecls BEGIN stmtlist END
    '''
    p[0] = (p[1],p[2],p[3],p[4],p[5])
    print(p[0])

def p_vardecls(p):
    '''
    vardecls : vardecl vardecls
             | e
    '''
    if len(p) == 2:
      p[0] = p[1]
    else:
      p[0] = (p[1],p[2])
    
def p_procdecls(p):
    '''
    procdecls : procdecl procdecls
              | e
    '''
    if len(p) == 2:
      p[0] = p[1]
    else:
      p[0] = (p[1],p[2])
    
def p_stmtlist(p):
    '''
    stmtlist : pstmt stmtlist
             | pstmt
    '''
    if len(p) == 2:
      p[0] = p[1]
    elif len(p) > 2:
      p[0] = (p[1], p[2])

def p_vardecl(p):
    'vardecl : VAR varlist SEMICOLON'
    p[0] = p[2]
    
def p_varlist(p):
    '''
    varlist : ID COMMA varlist
            | ID
    '''
    if len(p) == 2:
      p[0] = p[1]
    else:
      p[0] = (p[1],p[3])
    
def p_procdecl(p):
    'procdecl : PROC ID LPAREN paramlist RPAREN vardecls stmtlist'
    p[0] = (p[4], p[6], p[7])
    
def p_paramlist(p):
    '''
    paramlist : tparamlist
              | e
    '''
    p[0] = p[1]
    
def p_pstmt(p):
    '''
    pstmt : DLABEL
          | stmt SEMICOLON
    '''
    if len(p) == 2:
      p[0] = p[1]
    elif len(p) > 2:
      p[0] = (p[1], p[2])
    
def p_stmt(p):
    '''
    stmt : assign
         | condjump
         | jump
         | readstmt
         | printstmt
         | callstmt
         | RETURN
         | EXIT
    '''
    p[0] = p[1]

def p_assign(p):
    'assign : ID ASSIGN opd ARIT opd'
    p[0] = (p[2],p[1],(p[4],p[3],p[5]))

def p_condjump(p):
    'condjump : IF ID COMP ID GOTO ID' #Since id and label have the same requirements
    p[0] = (p[3],(p[1],p[3]),(p[5],p[4],p[6]))
    
def p_jump(p):
    'jump : GOTO ID'
    p[0] = (p[1], p[2])
    
def p_readstmt(p):
    'readstmt : READ ID'
    p[0] = (p[1], p[2])
    
def p_printstmt(p):
    '''
    printstmt : PRINT printarg
              | PRINTLN
    '''
    if len(p) == 2:
      p[0] = p[1]
    elif len(p) > 2: 
      p[0] = (p[1], p[2])
    
def p_printarg(p):
    '''
    printarg : ID
             | STR
    '''
    p[0] = p[1]
    
def p_callstmt(p):
    'callstmt : CALL ID LPAREN arglist RPAREN'
    p[0] = (p[2], p[1], (p[3], p[2], p[4]))
    
def p_arglist(p):
    '''arglist : targlist
               | e
    '''
    p[0] = p[1]

def p_targlist(p):
    'targlist : ID targ'
    p[0] = (p[2], p[1])

def p_targ(p):
  '''
  targ : COMMA ID targ
       | e
  '''
  if len(p) == 2:
    p[0] = None
  else:
    p[0] = (p[2], p[1], p[3])

def p_tparamlist(p):
    '''
    tparamlist : param COMMA tparamlist
               | param
    '''
    if len(p) == 2:
      p[0] = p[1]
    else:
      p[0] = (p[2], p[1], p[3])

def p_opd(p):
    '''
    opd : ID
        | NUM
    '''
    p[0] = p[1]

def p_param(p):
    'param : mode ID'
    p[0] = (p[1], p[2])
    
def p_mode(p):
    '''
    mode : IN
         | OUT
         | INOUT
    '''
    p[0] = p[1]

def p_e(p):
    'e : '
    p[0] = None

def p_error(p):
    print("Syntax error")

parser = yacc.yacc(start = "prog")

while True:
    try:
        s = input()
    except EOFError:
        break
    parser.parse(s)