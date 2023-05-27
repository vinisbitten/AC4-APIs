import mysql.connector
import requests
from flask import Flask, jsonify

app = Flask(__name__)

# Cria a conexão com o banco de dados MySQL
con = mysql.connector.connect(
    host='localhost',
    port=3309,
    database='db_ApiExterna',
    user='root',
    password='my-secret-pw'
)

# Verifica se a conexão foi estabelecida com sucesso
if con.is_connected():
    print('Conexão ao banco de dados MySQL estabelecida com sucesso!')

# Exemplo de rota que consulta o banco de dados
@app.route('/get_items', methods=['GET'])
def get_items():
    response = requests.get('http://localhost:5000/items')
    items = response.json()
    return jsonify(items)

@app.route('/create_item', methods=['POST'])
def create_item():
    data = {
        'id': 1,
        'name': 'New Item',
        'completed': False
    }
    response = requests.post('http://localhost:5000/items', json=data)
    item = response.json()
    return jsonify(item), 201

@app.route('/delete_item/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    response = requests.delete(f'http://localhost:5000/items/{item_id}')
    return '', 204

@app.route('/database', methods=['GET'])
def get_database_records():
    # Verifica se a conexão com o banco de dados está estabelecida
    if con.is_connected():
        # Cria o cursor para executar consultas
        cursor = con.cursor()

        # Executa a consulta
        cursor.execute('SELECT * FROM records')
        records = cursor.fetchall()

        # Formata os registros em uma lista de dicionários
        formatted_records = []
        for record in records:
            formatted_record = {
                'id': record[0],
                'name': record[1]
            }
            formatted_records.append(formatted_record)

        # Fecha o cursor
        cursor.close()

        return jsonify(formatted_records)
    else:
        return 'Erro: Não foi possível conectar ao banco de dados MySQL', 500

if __name__ == '__main__':
    app.run()