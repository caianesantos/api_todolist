# from datetime import date
from flask import Flask, jsonify, request
#importa o framework flask, ferramenta jsonify para retornar no formato json, request para (i/o) comunicação entre sistemas
from db import db, cursor



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

#--------------------TRATAMENTO DE ERRO----------------------------------

@app.errorhandler(400)
def bad_request(error=None):
    return jsonify({"Bad Request": "Você não pode criar uma tarefa sem título!"}), 400

@app.errorhandler(404)
def not_found_error(error=None):
    return jsonify({"Not Found": "Recurso não encontrado!"}), 404

@app.errorhandler(409)
def conflict(error=None):
    return jsonify({"Conflict": "Tarefa duplicada!"}), 409

@app.errorhandler(500)
def internal_server(error=None):
    return jsonify({"Internal Server": "Ocorreu um problema no servidor"}), 500
 # capturar possíveis erros de banco de dados

#-----------------------FUNÇÃO AUXILIAR--------------------------------------------
#Verificar se tarefa existe 
def buscar_task_id(id):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM tarefas WHERE id = %s", (id,))
        tarefa = cursor.fetchone()
        return tarefa # Retorna o dicionário da tarefa ou None
    
#--------------------ROTAS----------------------------------------------


#consultar (todos)
@app.route('/tarefas', methods=['GET'])
def consultar_task():
    """
    Consulta todas as tarefas existentes
    """
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM tarefas")
            todos = cursor.fetchall() #pega todas as linhas do banco
            if not todos:
                return not_found_error()
            else:
                return jsonify(todos), 200 
    except Exception as e:
        print(f"Erro: {e}")
        return internal_server()


# #consultar (id)
@app.route('/tarefas/<int:id>', methods=['GET'])
def consultar_id_tak(id):
    """
    Consulta tarefa pelo id
    """
    try:
        tarefa = buscar_task_id(id)
        if tarefa is None:
            return not_found_error()
        else:
            return jsonify(tarefa), 200
    except Exception as e:
        print(f"Erro: {e}")
        return internal_server()
    

#consultar (título)
@app.route('/tarefas/<string:titulo>', methods=['GET'])
def consultar_titulo_task (titulo):
    """
    Consulta uma tarefa pelo título
    """
    try:
        # A instrução 'with' abre o cursor e GARANTE que ele será fechado no final.
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM tarefas WHERE titulo = %s", (titulo,))
            tarefa = cursor.fetchall()
            if tarefa is None:
                return not_found_error()
            else:
                return jsonify(tarefa), 200
    except Exception as e:
        print(f"Erro: {e}")
        return internal_server()


#adicionar
@app.route('/tarefas', methods=['POST'])
def adicionar_task():
    """
    Adiciona uma nova tarefa
    """
    try:
        with db.cursor() as cursor:
            tarefas = request.json # Acessa os dados JSON
    
            if not tarefas.get("titulo"):
                return bad_request()
        
            sql = "INSERT INTO tarefas (titulo, descricao, status) VALUES (%s,%s,%s)"
            values = (tarefas["titulo"], tarefas.get("descricao"), False) 
            # se o usuario não digitar descrição, retornará None
            cursor.execute(sql,values) #consultar o banco de dados (insert into/ valores)
            db.commit() #salva no banco de dados

            return jsonify({"Created": "Tarefa adicionada!", "id": cursor.lastrowid}), 201
    except Exception as e:
        print(f"Erro: {e}")
        db.rollback() 
        return internal_server()


#atualizar status (id)
@app.route('/tarefas/att/<int:id>', methods=['PATCH'])
def atualizar_status(id):
    """
    atualizar status de uma tarefa para concluída (pesquisando por id)
    """
    try:
        tarefa = buscar_task_id(id)
        if tarefa is None:
            return not_found_error()
        else:
            cursor.execute("UPDATE tarefas SET status = 'Concluído' WHERE id = %s", (id,))
            db.commit()
            return jsonify({"Successful": "Status da tarefa atualizado com sucesso!"}), 200
    except Exception as e:
        print(f"Erro: {e}")
        return internal_server()


#deletar tarefa (id)
@app.route('/tarefas/del/<int:id>', methods=['DELETE'])
def deletar_task_id(id):
    """
    deletar uma tarefa pelo id
    """
    try:
        tarefa = buscar_task_id(id)
        if tarefa is None:
            return not_found_error() 
        else:
            cursor.execute("DELETE FROM tarefas WHERE id = %s", (id,))
            db.commit()
            return jsonify({"Successful": "Tarefa excluída com sucesso!"}), 200
    except Exception as e:
        print(f"Erro: {e}")
        return internal_server()

        

if __name__ == "__main__":
    app.run(port=5000, host="localhost", debug=True)