# from datetime import date
from db import db, cursor
from flask import Flask, jsonify, request
from status_task import task_list


    

#----------------------ROTAS------------------------------------------

app = Flask(__name__)


@app.route('/tarefas', methods=['GET'])
def consultar_task():
    """
    Consulta todas as tarefas existentes
    """
    cursor.execute("SELECT * FROM tarefas")
    todos = cursor.fetchall() #pega todas as linhas do banco
    return jsonify(todos)    

@app.route('/tarefas/<int:id>', methods=['GET'])
def consultar_id_taks(id):
    """
    Consulta tarefa pelo id
    """
    cursor.execute("SELECT * FROM tarefas WHERE id = %s", (id,))
    tarefa = cursor.fetchone()
    return jsonify(tarefa)

@app.route('/tarefas', methods=['POST'])
def adicionar_task():
    """
    Adiciona uma nova tarefa
    """
    tarefas = request.json # Acessa os dados JSON
    sql = "INSERT INTO tarefas (titulo, descricao, conclusao) VALUES (%s,%s,%s)"
    values = (tarefas["titulo"], tarefas["descricao"], False)
    cursor.execute(sql,values) #consultar o banco de dados (insert into/ valores)
    db.commit() #salva no banco de dados
    return jsonify({"message": "Tarefa adicionada!", "id": db.cursor.lastrowid}), 201

if __name__ == "__main__":
    app.run(port=5000, host="localhost", debug=True)