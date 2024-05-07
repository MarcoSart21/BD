import ply.yacc as yacc
from analizador_lexico import tokens
from analizador_lexico import lexer

# Resultado del análisis
resultado_gramatica = []

def p_create_database(t):
    'declaracion : CREATE DATABASE IDENTIFICADOR PUNTOCOMA'
    print("CREATE DATABASE encontrado:", t[3])
    t[0] = ("CREATE DATABASE encontrado",)
        
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