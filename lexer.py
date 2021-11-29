import lex
import yacc

tokens = ['NUM', 'STR', 'ID', 'LABEL', 'KEYWORD', 'ARIT', 'COMP']

t_ignore = r' '
t_ARIT = r'\+|\-|\*|\/'
t_COMP = r'<|>|<=|>=|=|<>'

def t_KEYWORD(t):
    r'call|println|print|read|goto|if|return|exit|in|out|inout|proc|var|begin|end'
    return t

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_STR(t):
    r'"[^][^]*"|\'[^][^]*\''
    return t

def t_LABEL(t):
    r'[a-zA-Z0-9][a-zA-Z0-9_]*:'
    return t

def t_ID(t):
    r'[a-zA-Z0-9][a-zA-Z0-9_]*'
    return t

def t_error(t):
    print("Invalid character: "+str(t)[16]+'\nPlease check and try again')
    t.lexer.skip(1)

lexer = lex.lex()

lexer.input('$')

while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)