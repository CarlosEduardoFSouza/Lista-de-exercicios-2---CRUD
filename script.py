from mysql.connector import (connection)
from flask import Flask
from flask import jsonify
from matplotlib.font_manager import json_dump
from flask import request


app = Flask(__name__)

from datetime import date

con = connection.MySQLConnection(host='localhost', user='root', password='C@rlinhos10', database='agenda')

cursor = con.cursor()

@app.route("/", methods=["GET"])
def orientacoes():
    return '''
    <style type="text/css">
        body {
            background-color: black;
            color: white;
        }
    </style>
    <html>
        <body>
            <h1>Bem vindo</h1>
            <p>Para ver os estados /estados<p>
            <p>Para ver os estados agrupados /estadosAgrupados<p>
        </body>
    </html>
    '''

@app.route("/contatos", methods=["GET"])
def listarEstados():
    comando_sql = "SELECT * FROM contatos"
    cursor.execute(comando_sql)
    dados = cursor.fetchall()
    print("Contatos")
    return jsonify(dados),200


@app.route("/estadosAgrupados", methods=["GET"])
def listarGrupoContatos():
    comando_sql = "SELECT empresa, GROUP_CONCAT(nome) FROM contatos GROUP BY empresa;"
    cursor.execute(comando_sql)
    dados = cursor.fetchall()
    return jsonify(dados),200

@app.route("/estadoInserir", methods=['POST'])
def inserirContato():
    nome = request.get_json().get('nome')
    empresa = request.get_json().get('empresa')
    telefone = request.get_json().get('telefone')
    email = request.get_json().get('email')
    
    comando_sql = f"INSERT INTO contatos (nome, empresa, telefone, email) VALUES {nome, empresa,telefone, email}"
    cursor.execute(comando_sql) 
    con.commit()
    return jsonify('Inserido com sucesso.'), 201
    
@app.route("/contatosAlterar/<int:id>", methods=['PUT'])
def alterarContato(id):
    email = request.get_json().get('email')
    comando_sql = f"UPDATE contatos SET email = '{email}' WHERE id = {id}"
    cursor.execute(comando_sql) 
    con.commit()
    return jsonify(x), 200
    
@app.route("/estadoDeletar/<int:id>", methods=['DELETE'])
def deletarContato(id):
    comando_sql = f"DELETE FROM contatos WHERE id = {id}"
    cursor.execute(comando_sql) 
    con.commit()
    return "Registro Removido!", 204
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

con.close()