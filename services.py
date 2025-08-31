from db import *

#-----------------------FUNÇÃO AUXILIAR--------------------------------------------
#Verificar se tarefa existe 
def buscar_task_id(id):
    with db.cursor() as cursor:
        cursor.execute("SELECT * FROM tarefas WHERE id = %s", (id,))
        tarefa = cursor.fetchone()
        return tarefa # Retorna o dicionário da tarefa ou None
    