from flask import Flask, request, jsonify, render_template
import analizador_lexico as lex

import CrearBD as yacc
import Use as yacc_Use
import CrearTabla as yacc_CrearTabla
import InsertarRegistro as yacc_InsertarRegistro
import Update as yacc_Update
import DropBD as yacc_DropBD

import pyodbc

app = Flask('app')
current_database = None  # Variable global para almacenar la base de datos seleccionada

# Establecer la conexión a la base de datos
connection = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=DESKTOP-PODC17J\SQLEXPRESS;UID=sa;PWD=osito2020', autocommit=True)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/api/v1/lexer', methods=['POST'])
def lexer():
    data = request.get_json()
    code = data.get('code')

    lex.lexer.input(code)

    tokens = []
    while True:
        tok = lex.lexer.token()
        if not tok:
            break
        tokens.append({
            'type': tok.type,
            'value': tok.value,
            'line': tok.lineno,
            'lexpos': tok.lexpos
        })

    print("Code:", code)
    print("Tokens", tokens)
    
    return render_template('result.html', tokens = tokens)


@app.route('/api/v1/parser', methods=['POST'])
def parser():
    data = request.get_json()
    code = data.get('code')

    command_type = data.get('commandType')

    syntax_errors = []

    if command_type == 'createDatabase':
        syntax_errors = yacc.prueba_sintactica(code)
    elif command_type == 'useDatabase':
        syntax_errors = yacc_Use.prueba_sintactica(code)
    elif command_type == 'createTable':
        syntax_errors = yacc_CrearTabla.prueba_sintactica(code)
    elif command_type == 'insertRecord':
        syntax_errors = yacc_InsertarRegistro.prueba_sintactica(code)
    elif command_type == 'updateRecord':
        syntax_errors = yacc_Update.prueba_sintactica(code)
    elif command_type == 'dropDatabase':
        syntax_errors = yacc_DropBD.prueba_sintactica(code)

    if syntax_errors:
        return render_template('resultsintaxis.html', errors=syntax_errors)
    else:
        errors = ejecutar_comando_sql(code)
        if not errors:
            return render_template('resultsintaxis.html', success_message="Sintaxis correcta.", message="Comando SQL ejecutado correctamente")
        else:
            return render_template('resultsintaxis.html', code=code, errorsql=errors)
    
    
    
def ejecutar_comando_sql(sql):
    global current_database
    try:
        global connection

        # Imprimir el nombre de la base de datos actual antes de USE
        cursor = connection.cursor()
        cursor.execute('SELECT DB_NAME() AS DatabaseName')
        database_name_before = cursor.fetchone()[0]
        print("Base de datos actual antes de USE:", database_name_before)

        # Ejecutar el comando SQL
        cursor.execute(sql)

        # Ejecutar el comando USE para cambiar la base de datos
        if sql.strip().lower().startswith("use"):
            current_database = sql.strip().lower().split(" ")[1].strip(";")
            print("Base de datos cambiada a:", current_database)

        # Imprimir el nombre de la base de datos actual después de USE
        cursor.execute('SELECT DB_NAME() AS DatabaseName')
        database_name_after = cursor.fetchone()[0]
        print("Base de datos actual después de USE:", database_name_after)

        return []
    
    
    except pyodbc.Error as e:
        sql_state = e.args[0].split()[0]  # Obtenemos el estado SQL del error
        if sql_state == '42000':  # Error de base de datos ya existente
            error_message = "Error: La base de datos ya existe"
        elif sql_state == '42S01':  # Error de tabla ya existente
            error_message = "Error: Ya existe la tabla"
        else:
            error_message = "Error al ejecutar el comando SQL: " + str(e)
        return [error_message]
    
    # except Exception as e:
    #     print("Error al ejecutar el comando SQL:", e)
    #     return False


if __name__ == '__main__':
    app.run(debug=True, port=4000)