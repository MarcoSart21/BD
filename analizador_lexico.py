import ply.lex as lex

resultado_lexema = []
errores_lexicos = []

# Palabras clave
reserved = {
    'CREATE': 'CREATE',
    'DATABASE': 'DATABASE',
    'DROP': 'DROP',
    'USE': 'USE',
    'TABLE': 'TABLE',
    'INSERT': 'INSERT',
    'INTO': 'INTO',
    'VALUES': 'VALUES',
    'VARCHAR': 'VARCHAR',
    'INT': 'INT',
    'FLOAT': 'FLOAT',
    
    'DELETE': 'DELETE',
    'FROM': 'FROM',
    'UPDATE': 'UPDATE',
    'SET': 'SET',
    'WHERE': 'WHERE',
    'AND': 'AND',
    'OR': 'OR',
    'ALTER': 'ALTER',
    'TRUNCATE': 'TRUNCATE',
    'COMMIT': 'COMMIT',
    'ROLLBACK': 'ROLLBACK',
}

# Lista de tokens
tokens = [
    'IDENTIFICADOR',
    'NUMBER',
    'STRING',
    'PUNTOCOMA',
    'LPAREN',
    'RPAREN',
    'COMA',
    'IGUAL',
] + list(reserved.values())

# Expresiones regulares para tokens simples
t_STRING = r"'[^\']*'"
t_PUNTOCOMA = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMA = r','
t_IGUAL = r'='

# Regla para identificadores
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z]*'
    if t.value.upper() in reserved:  # Verificar si es una palabra reservada
        t.type = reserved[t.value.upper()]  # Asignar el tipo de token correspondiente a la palabra reservada
    else:
        t.type = 'IDENTIFICADOR'  # Asignar el tipo de token como IDENTIFICADOR si no es una palabra reservada
    return t


# Regla para números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar caracteres como espacios y tabulaciones
t_ignore = ' \t'

# Manejo de errores
def t_error(t):
    print("Carácter inválido '%s' en la posición %d" % (t.value[0], t.lexpos))
    t.lexer.skip(1)

# Prueba de ingreso
def prueba(data):
    global resultado_lexema

    analizador = lex.lex()
    analizador.input(data)

    resultado_lexema.clear()
    while True:
        tok = analizador.token()
        if not tok:
            break
        estado = "Linea {:4} Tipo {:16} Valor {:16} Posicion {:4}".format(str(tok.lineno), str(tok.type), str(tok.value), str(tok.lexpos))
        resultado_lexema.append(estado)
    return resultado_lexema


# Construir el analizador léxico
lexer = lex.lex()

if __name__ == '__main__':
    while True:
        data = input("Ingrese: ")
        prueba(data)
        print(resultado_lexema)
