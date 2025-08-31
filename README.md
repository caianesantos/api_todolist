# API de Tarefas (To-Do List)

Esta é uma API simples para gerenciamento de tarefas, desenvolvida em Python com o framework Flask. Ela permite criar, consultar, atualizar e deletar tarefas, utilizando um banco de dados MySQL para persistência dos dados.

Este guia descreve como configurar, executar e testar o projeto em um ambiente de desenvolvimento local.

## Pré-requisitos

Antes de começar, certifique-se de que você tem os seguintes softwares instalados:

  * **Python 3.8+**
  * **Git**
  * Um servidor de banco de dados **MySQL**
  * **Postman** (ou similar) para testar os endpoints.

## Guia de Instalação e Configuração

Siga os passos abaixo para ter a API rodando na sua máquina.

### 1\. Obtenha o Código-Fonte

Clone o repositório do projeto para sua máquina local usando Git:

```bash
git clone <URL_DO_SEU_REPOSITORIO_GIT>
cd <NOME_DO_DIRETORIO_DO_PROJETO>
```

### 2\. Configure o Ambiente Python

É uma forte recomendação usar um ambiente virtual para isolar as dependências do projeto.

**Crie e ative o ambiente virtual:**

```bash
# No Windows
python -m venv ambiente
.\ambiente\Scripts\activate

# No macOS / Linux
python3 -m venv ambiente
source ambiente/bin/activate
```

**Instale as dependências necessárias a partir do arquivo `requirements.txt`:**

```bash
pip install -r requirements.txt
```

### 3\. Crie e Configure o Banco de Dados MySQL

**1. Crie o Banco de Dados:** Acesse seu servidor MySQL e crie um novo banco de dados. [cite\_start]O nome `todolist` é recomendado para seguir o padrão do projeto. [cite: 1]

```sql
CREATE DATABASE todolist;
```

**2. Crie a Tabela `tarefas`:** Após criar e selecionar o banco de dados (`USE todolist;`), execute o comando SQL abaixo para criar a tabela que armazenará as tarefas:

```sql
CREATE TABLE tarefas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descricao TEXT,
    status VARCHAR(50) DEFAULT 'Pendente',
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_att TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 4\. Conecte a Aplicação ao Banco de Dados

**1. Localize o arquivo `db.py`** na raiz do projeto.

**2. Edite o arquivo** com as suas credenciais do MySQL. Substitua os placeholders (`'...'`) pelas suas informações locais.

```python
# db.py
import mysql.connector

try:
    db = mysql.connector.connect(
        host='localhost',          # Geralmente 'localhost' para ambiente local
        user='seu_usuario_mysql',  # <-- SUBSTITUA PELO SEU USUÁRIO
        password='sua_senha_mysql',# <-- SUBSTITUA PELA SUA SENHA
        database='todolist'        # O nome do banco de dados criado no passo 3
        charset="utf8mb4",         # Garante suporte a emojis e caracteres especiais
        use_unicode=True           # Garante que o texto seja tratado corretamente
    )

    cursor = db.cursor(dictionary=True)
    print("Conexão com o banco de dados MySQL bem-sucedida!")

except mysql.connector.Error as e:
    print(f"Erro ao conectar com o MySQL: {e}")
    exit()
```

### 5\. Execute a API

Com o ambiente e o banco de dados configurados, inicie o servidor Flask:

```bash
python main.py
```

O terminal indicará que o servidor está rodando em `http://localhost:5000`.

## Guia de Uso com Postman

A seguir, um passo a passo de como testar cada endpoint usando o Postman.

### Método POST: Criar uma Nova Tarefa

1.  Abra uma nova requisição no Postman.
2.  [cite\_start]Mude o método HTTP para **POST**. [cite: 234]
3.  [cite\_start]Insira a URL do endpoint: `http://localhost:5000/tarefas`. [cite: 233]
4.  Vá para a aba **Headers** e adicione a seguinte chave-valor:
      * [cite\_start]**Key**: `Content-Type` [cite: 237]
      * [cite\_start]**Value**: `application/json` [cite: 238]
5.  [cite\_start]Vá para a aba **Body**, selecione a opção **raw** e mude o formato para **JSON**. [cite: 240, 241]
6.  [cite\_start]Escreva o corpo da requisição com os dados da tarefa: [cite: 242]
    ```json
    {
        "titulo": "Aprender a usar o Postman",
        "descricao": "Criar um exemplo de requisição POST para a API de tarefas."
    }
    ```
7.  Clique em **Send**.

### Método GET: Consultar Tarefas

#### [cite\_start]Consultar todas as tarefas [cite: 153]

1.  [cite\_start]Mude o método HTTP para **GET**. [cite: 156]
2.  [cite\_start]Insira a URL: `http://localhost:5000/tarefas`. [cite: 155]
3.  Clique em **Send**.

#### [cite\_start]Consultar por ID [cite: 178]

1.  [cite\_start]Mude o método HTTP para **GET**. [cite: 181]
2.  [cite\_start]Insira a URL, substituindo `<id>` pelo número desejado: `http://localhost:5000/tarefas/<id>`. [cite: 180]
3.  Clique em **Send**.

#### [cite\_start]Consultar por Título [cite: 190]

1.  [cite\_start]Mude o método HTTP para **GET**. [cite: 193]
2.  [cite\_start]Insira a URL, substituindo `<titulo>` pelo texto desejado: `http://localhost:5000/tarefas/<titulo>`. [cite: 192]
3.  Clique em **Send**.

#### [cite\_start]Consultar por Data [cite: 202, 218]

1.  [cite\_start]Mude o método HTTP para **GET**. [cite: 206]
2.  Insira a URL: `http://localhost:5000/tarefas/data`.
3.  [cite\_start]Vá para a aba **Params** e adicione as seguintes chaves-valor: [cite: 212]
      * [cite\_start]**Key**: `tipo`, **Value**: `criacao` ou `atualizacao` [cite: 214, 215, 228, 229]
      * [cite\_start]**Key**: `data`, **Value**: `<AAAA-MM-DD>` (ex: `2025-08-22`) [cite: 216, 217]
4.  Clique em **Send**.

### [cite\_start]Método PATCH: Atualizar uma Tarefa [cite: 245]

1.  [cite\_start]Mude o método HTTP para **PATCH**. [cite: 249]
2.  [cite\_start]Insira a URL, substituindo `<id>`: `http://localhost:5000/tarefas/att/<id>`. [cite: 248]
3.  **Para atualizar título/descrição:**
      * Vá para a aba **Body**, selecione **raw** e **JSON**.
      * Insira apenas os campos que deseja alterar:
        ```json
        {
            "titulo": "Novo título atualizado"
        }
        ```
4.  **Para marcar como "Concluído":**
      * [cite\_start]Você pode deixar o corpo da requisição vazio (none). [cite: 250]
5.  Clique em **Send**.

### [cite\_start]Método DELETE: Excluir uma Tarefa [cite: 252]

1.  [cite\_start]Mude o método HTTP para **DELETE**. [cite: 256]
2.  [cite\_start]Insira a URL, substituindo `<id>`: `http://localhost:5000/tarefas/del/<id>`. [cite: 255]
3.  Clique em **Send**. [cite\_start]O retorno esperado é uma mensagem de sucesso. [cite: 259, 260]