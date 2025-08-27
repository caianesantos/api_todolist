from datetime import datetime
from flask import Flask, jsonify, request
#importa o framework flask, ferramenta jsonify para retornar no formato json, request para (i/o) comunicação entre sistemas
from db import db, cursor



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

#--------------------TRATAMENTO DE ERRO----------------------------------

@app.errorhandler(400)
def bad_request(error=None):
    """
    Para informar que existem campos inválidos, como:
        - Tentativa de criar tarefa sem título ou sem parâmetro;
        - Tipo de data inválido;
    """
    return jsonify({"Bad Request": "Existem campos inválidos!"}), 400

@app.errorhandler(404)
def not_found_error(error=None):
    """
    Mensagem de erro para informar que uma tarefa não foi encontrada
    """
    return jsonify({"Not Found": "Tarefa não encontrada!"}), 404

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


#consultar por data de criação
@app.route('/tarefas/data')
def consultar_por_data():
    """
    Consulta tarefas por um campo de data específico (criação ou atualização).
    """
     # 1. Pegar os parâmetros da URL
    tipo_data = request.args.get('tipo') # Pega o valor de 'tipo'
    data_str = request.args.get('data')  # Pega o valor de 'data'

    # 2. Validar a entrada
    if not tipo_data or not data_str:
        return jsonify({"Erro": "Parâmetros 'tipo' e 'data' são obrigatórios."}), 400

    # 3. Mapear o 'tipo' para o nome real da coluna no banco de dados
    #    Isso é CRUCIAL para a segurança e evita Injeção de SQL!
    colunas_permitidas = {
        'criacao': 'data_criacao',
        'atualizacao': 'data_att'
        # Adicione outros campos de data aqui no futuro, como 'conclusao': 'data_conclusao'
    }
    if tipo_data not in colunas_permitidas:
        return jsonify({"Erro": "Tipo de data inválido. Use 'criacao' ou 'atualizacao'."}), 400

    coluna_sql = colunas_permitidas[tipo_data] # Pega o nome seguro da coluna

    # 4. Validar e converter a data (mesmo código de antes)
    try:
        data_pesquisa = datetime.strptime(data_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"Erro": "Formato de data inválido. Use AAAA-MM-DD."}), 400
    try:
        with db.cursor() as cursor:
            # Construir a query dinamicamente, mas de forma segura
            # ATENÇÃO: Nunca passe o nome da coluna como um parâmetro (%)
            # Por isso validamos na etapa 3.
            query = f"SELECT * FROM tarefas WHERE DATE({coluna_sql}) = %s"
            cursor.execute(query, (data_pesquisa,))
            
            tarefas = cursor.fetchall()
            
            if not tarefas:
                return not_found_error()
            else:
                return jsonify(tarefas), 200
                
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
            values = (tarefas["titulo"], tarefas.get("descricao"), 'Pendente')
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
# adicionar atualizar (em andamento)

#atualizar título e/ou descrição
@app.route('/tarefas/att/<int:id>', methods=['PATCH'])
def att_titulo_desc(id):
    try:
        tarefa = buscar_task_id(id)
        if tarefa is None:
            return not_found_error()
    
        else:
            partes_query = []
            valores = []
            dados_recebidos = request.get_json()

        #adiciona um novo titulo, caso tenha sido passado
            if 'titulo' in dados_recebidos:
                partes_query.append("titulo = %s")
                valores.append(dados_recebidos['titulo'])

        #adiciona uma nova descrição, caso tenha sido passada
            if 'descricao' in dados_recebidos:
                partes_query.append("descricao = %s")
                valores.append(dados_recebidos['descricao'])
            
            #Validação para evitar erro com query vazia.
            if not partes_query:
                return jsonify({"Error": "Nenhum campo válido para atualização fornecido"}), 400
            
            #Montando a query final
            string_set = ", ".join(partes_query)
            query_final = f"UPDATE tarefas SET {string_set} WHERE id = %s"
            #junta tudo o que recebeu (titulo e descricao)
           
           #Adicionando o id e executando
            valores.append(id)
            cursor.execute(query_final, tuple(valores))
            db.commit()
            return jsonify({"Successful": "Tarefa atualizada com sucesso!"}), 200
    #Agora, a query_final (o comando dinâmico) é executada com os valores correspondentes 
    # (a lista dinâmica). Usamos tuple(valores) porque a maioria das bibliotecas de 
    # banco de dados espera uma tupla de parâmetros, não uma lista.

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