import ply.yacc as yacc
from analizador_lexico import tokens
from analizador_lexico import lexer

# Resultado del análisis
resultado_gramatica = []

def p_create_table(t):
    'declaracion : CREATE TABLE IDENTIFICADOR LPAREN columns RPAREN PUNTOCOMA'
    print("CREATE TABLE encontrado:", t[3])
    t[0] = ("CREATE TABLE encontrado", t[3], t[5])

def p_columns(t):
    '''columns : column
                | columns COMA column'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[3]]

def p_column(t):
    'column : IDENTIFICADOR datatype'
    t[0] = (t[1], t[2])

def p_datatype(t):
    '''datatype : VARCHAR LPAREN NUMBER RPAREN
                | INT
                | FLOAT'''
    if len(t) == 5:
        t[0] = f"{t[1]}({t[3]})"
    else:
        t[0] = t[1]


def p_error(t):
    global resultado_gramatica
    if t:
        resultado = "Error sintáctico de tipo {} en el valor {}".format(str(t.type), str(t.value))
    else:
        resultado = "Error sintáctico: Token inválido"
    print(resultado)
    resultado_gramatica.append(resultado)


# Instanciamos el analizador léxico
parser = yacc.yacc()

def prueba_sintactica(data):
    global resultado_gramatica
    resultado_gramatica.clear()
    
    # Realizar el análisis sintáctico en el código completo
    parser.parse(data)

    return resultado_gramatica

if __name__ == '_main_':
    while True:
        try:
            s = input('Ingrese el comando CREATE DATABASE: ')
        except EOFError:
            continue
        if not s:  
            continue
        
        gram = parser.parse(s)
        print("Resultado ", gram)
        prueba_sintactica(s)