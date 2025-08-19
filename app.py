# 1. Objetivo - Criar uma api que cria, gerencia e consulta tarefas (CRUD)
# 2. URL base - localhost
# 3. Endpoints:
    # - localhost/tasks (POST) - Criar tarefa (recebe título e descrição no corpo da requisição)
    # - localhost/tasks (GET) - retornar uma lista de tarefas existentes
    # - localhost/tasks/<id> (GET) - retornar detalhes de uma tarefa específica (identificada pelo id)
    # - localhost/tasks/<id> (PATCH) - atualizar o status de uma tarefa para concluída (done: true)
    # - localhost/tasks/<id> (DELETE) - remove uma tarefa específica do banco de dados
# 4. Recursos: Tasks

# import mysql.connector

# conexao = mysql.connector.connect(
#     host="localhost",
#     user="seu_usuario",
#     password="sua_senha",
#     database="seu_banco"
# )

# cursor = conexao.cursor()

import datetime
from flask import Flask, jsonify, request
#importa o framework flask, ferramenta jsonify para retornar no formato json, request para (i/o) comunicação entre sistemas

app = Flask(__name__)

tarefas = [
    {
        'id': int,
        'titulo': str,
        'descricao': str,
        'conclusao': bool,
        'hora_criacao': datetime
    }
]

#consultar (todos)
@app.route('/tarefas')
def consultar_task():
    return jsonify(tarefas)    

#consultar (id)
#editar
#excluir
app.run(port=5000,host='localhost',debug=True)

