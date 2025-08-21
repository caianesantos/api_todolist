# from datetime import date
from db import db, cursor
from flask import Flask, jsonify, request

app = Flask(__name__)

#consultar (todos)
@app.route('/tarefas', methods=['GET'])
def consultar_task():
    cursor.execute("SELECT * FROM tarefas")
    todos = cursor.fetchall() #pega todas as linhas do banco
    return jsonify(todos)    


@app.route('/tarefas', methods=['POST'])
def adicionar_task():
    tarefas = request.json # Acessa os dados JSON
    sql = "INSERT INTO tarefas (titulo, descricao, conclusao) VALUES (%s,%s,%s)"
    values = (tarefas["titulo"], tarefas["descricao"], False)
    cursor.execute(sql,values) #consultar o banco de dados (insert into/ valores)
    db.commit() #salva no banco de dados
    return jsonify({"message": "Tarefa adicionada!", "id": db.cursor.lastrowid}), 201

if __name__ == "__main__":
    app.run(port=5000, host="localhost", debug=True)