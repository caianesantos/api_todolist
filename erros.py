from flask import Flask, jsonify


app = Flask(__name__)

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