import ply.yacc as yacc
from analizador_lexico import tokens
from analizador_lexico import lexer

# Resultado del análisis
resultado_gramatica = []

#REGLAS PARA UPDATE Y DELETE
def p_delete(t):
    '''declaracion : DELETE FROM IDENTIFICADOR PUNTOCOMA
                    | DELETE FROM IDENTIFICADOR WHERE condicion PUNTOCOMA'''
    if len(t) == 5:
        print("DELETE FROM encontrado:", t[3])
        t[0] = ("DELETE FROM encontrado", t[3])
    else:
        print("DELETE FROM encontrado con condición:", t[3], t[5])
        t[0] = ("DELETE FROM encontrado con condición", t[3], t[5])

def p_update(t):
    'declaracion : UPDATE IDENTIFICADOR SET asignaciones WHERE condicion PUNTOCOMA'
    print("UPDATE encontrado:", t[2])
    t[0] = ("UPDATE encontrado", t[2], t[4], t[6])

def p_asignaciones(t):
    '''asignaciones : asignacion
                    | asignaciones COMA asignacion'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[3]]

def p_asignacion(t):
    'asignacion : IDENTIFICADOR IGUAL value'
    t[0] = (t[1], t[3])

def p_condicion(t):
    'condicion : IDENTIFICADOR IGUAL value'
    t[0] = (t[1], t[3])

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
            s = input('Ingrese el comando UPDATE O DELETE: ')
        except EOFError:
            continue
        if not s:  
            continue
        
        gram = parser.parse(s)
        print("Resultado ", gram)
        prueba_sintactica(s)