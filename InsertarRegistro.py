import ply.yacc as yacc
from analizador_lexico import tokens
from analizador_lexico import lexer

# Resultado del análisis
resultado_gramatica = []

#INSERTAR REGISTROS
def p_insert_into(t):
    'declaracion : INSERT INTO IDENTIFICADOR VALUES valores PUNTOCOMA'
    print("INSERT INTO encontrado:", t[3])
    t[0] = ("INSERT INTO encontrado", t[3], t[5])

def p_valores(t):
    '''valores : LPAREN values RPAREN
                | valores COMA LPAREN values RPAREN'''
    if len(t) == 4:
        t[0] = [t[2]]
    else:
        t[0] = t[1] + [t[4]]

def p_values(t):
    '''values : value
                | values COMA value'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[3]]

def p_value(t):
    '''value : NUMBER
            | STRING'''
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
            s = input('Ingrese el comando INSERT INTO: ')
        except EOFError:
            continue
        if not s:  
            continue
        
        gram = parser.parse(s)
        print("Resultado ", gram)
        prueba_sintactica(s)