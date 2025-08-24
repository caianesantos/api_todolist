# from datetime import date
from db import db, cursor
from flask import Flask, jsonify, request
from status_task import task_list


    

#----------------------ROTAS------------------------------------------

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

#--------------------TRATAMENTO DE ERRO----------------------------------

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"Bad Request": "Recurso incompleto!"}), 404

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"Error Not Found": "Recurso não encontrado!"}), 404


#--------------------ROTAS----------------------------------------------

#consultar (todos)
@app.route('/tarefas', methods=['GET'])
def consultar_task():
    """
    Consulta todas as tarefas existentes
    """
    cursor.execute("SELECT * FROM tarefas")
    todos = cursor.fetchall() #pega todas as linhas do banco
    if not todos:
        return jsonify({"Not Found": "Nenhuma tarefa encontrada!"}), 404 
    else:
        return jsonify(todos), 200 


# #consultar (id)
@app.route('/tarefas/<int:id>', methods=['GET'])
def consultar_id_tak(id):
    """
    Consulta tarefa pelo id
    """
    cursor.execute("SELECT * FROM tarefas WHERE id = %s", (id,))
    tarefa = cursor.fetchone()
    if tarefa is None:
        return jsonify({"Not Found": "Tarefa nao encontrada!"}), 404 
    else:
        return jsonify(tarefa), 200


#adicionar
@app.route('/tarefas', methods=['POST'])
def adicionar_task():
    """
    Adiciona uma nova tarefa
    """
    tarefas = request.json # Acessa os dados JSON

    if not tarefas.get("titulo"):
        return jsonify({"Bad Request": "A tarefa precisa de um titulo!"}), 400
    
    sql = "INSERT INTO tarefas (titulo, descricao, status) VALUES (%s,%s,%s)"
    values = (tarefas["titulo"], tarefas["descricao"], False)
    cursor.execute(sql,values) #consultar o banco de dados (insert into/ valores)
    db.commit() #salva no banco de dados

    return jsonify({"Created": "Tarefa adicionada!", "id": db.cursor.lastrowid}), 201


#atualizar status
@app.route('/tarefas/att/<int:id>', methods=['PATCH'])
def atualizar_status(id):
    """
    atualizar status de uma tarefa para concluída
    """
    cursor.execute("SELECT * FROM tarefas WHERE id = %s", (id,))
    tarefa = cursor.fetchone()
    if tarefa is None:
        return jsonify({"Not Found": "Tarefa nao encontrada!"}), 404 
    else:
        cursor.execute("UPDATE tarefas SET status = 'Concluído' WHERE id = %s", (id,))
        db.commit()
        return jsonify({"Successful": "Status da tarefa atualizado com sucesso!"}), 200
    

    #deletar tarefa
@app.route('/tarefas/dell/<int:id>', methods=['DELETE'])
def deletar_task(id):
    """
    deletar uma tarefa pelo id
    """
    cursor.execute("SELECT * FROM tarefas WHERE id = %s", (id,))
    tarefa = cursor.fetchone()
    if tarefa is None:
        return jsonify({"Not Found": "Tarefa nao encontrada!"}), 404 
    else:
        cursor.execute("DELETE FROM tarefas WHERE id = %s", (id,))
        db.commit()
        return jsonify({"Successful": "Tarefa excluída com sucesso!"}), 200
    
    

if __name__ == "__main__":
    app.run(port=5000, host="localhost", debug=True)