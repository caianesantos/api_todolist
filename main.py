import mysql.connector as mysql
import datetime
from flask import Flask, jsonify, request

bd = mysql.connect(
    host= 'localhost',
    user= 'root',
    password= '123456',
    port= '3306',
    database= 'todolist'
) #conectar ao banco de dados

cursor = bd.cursor() 

cursor.execute('SELECT * FROM tarefas') #executar comandos

resultado = cursor.fetchall()
print(resultado)


# app = Flask(__name__)

# #consultar (todos)
# @app.route('/tarefas', methods=['GET'])
# def consultar_task():
#     return jsonify(tarefas)    

# #consultar (id)
# def consultar_id_taks(id):
#     return (tarefas)
# #editar
# #excluir

# if __name__ == "__main__":
#     app.run(port=5000, host="localhost", debug=True)