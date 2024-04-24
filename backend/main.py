import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# MySQL database configuration
db_config = {
    'user': 'root',
    'password': 'root',
    'host': '127.0.0.1',
    'database': 'bdracks'
}



def insert_drawer(nome, descricao, estado, rack_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "INSERT INTO Gaveta (nome, descricao, estado, Rack_idRack) VALUES (%s, %s, %s, %s)"
        values = (nome, descricao, estado, rack_id)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print('Error inserting drawer information:', str(e))
        return False


@app.route('/')
def hello():
    return jsonify({'message': 'Welcome to the API'})


def insert_rack(nome, localizacao, descricao):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "INSERT INTO Rack (nome, localizacao, descricao) VALUES (%s, %s, %s)"
        values = (nome, localizacao, descricao)
        cursor.execute(query, values)
        connection.commit()
        rack_id = cursor.lastrowid  # Obtém o ID do Rack recém-inserido
        cursor.close()
        connection.close()
        return rack_id
    except Exception as e:
        print('Error inserting rack information:', str(e))
        return None




@app.route('/add_rack', methods=['POST'])
def add_rack():

    if request.method == 'POST':
        data = request.get_json()
        if 'nome' in data and 'localizacao' in data and 'descricao' in data:
            nome = data['nome']
            localizacao = data['localizacao']
            descricao = data['descricao']
            rack_id = insert_rack(nome, localizacao, descricao)  # Obtém o ID do Rack inserido
            if rack_id is not None:
                # Insira as Gavetas associadas a esse Rack usando o rack_id
                gaveta_data = data.get('gavetas', [])  # Suponhamos que as gavetas sejam fornecidas como uma lista
                for gaveta in gaveta_data:
                    if 'nome' in gaveta and 'descricao' in gaveta and 'estado' in gaveta:
                        gaveta_nome = gaveta['nome']
                        gaveta_descricao = gaveta['descricao']
                        gaveta_estado = gaveta['estado']
                        if insert_drawer(gaveta_nome, gaveta_descricao, gaveta_estado, rack_id):
                            print(f"Gaveta inserida com sucesso para o Rack ID {rack_id}")
                        else:
                            print("Falha ao inserir a gaveta.")
                return jsonify({'message': 'Rack e gavetas associadas inseridos com sucesso'}), 201
            else:
                return jsonify({'message': 'Failed to add the rack'}), 500
        else:
            return jsonify({'message': 'Invalid data'}), 400




# Add a gaveta
@app.route('/add_drawer', methods=['POST'])
def add_drawer():

    print(request.get_json())
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        if 'nome' in data and 'descricao' in data and 'estado' in data and 'Rack_idRack' in data:
            nome = data['nome']
            descricao = data['descricao']
            estado = data['estado']
            rack_id = data['Rack_idRack']  # Extrair o valor de Rack_idRack

            if insert_drawer(nome, descricao, estado, rack_id):
                return jsonify({'message': 'Drawer added successfully'}), 201
            else:
                return jsonify({'message': 'Failed to add the drawer'}), 500
        else:
            return jsonify({'message': 'Invalid data'}), 400




# Update a gaveta by ID
@app.route('/update_gaveta', methods=['PUT'])
def update_gaveta():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        data = request.get_json()
        gaveta_id = data.get('id')
        updated_name = data.get('nome')
        updated_description = data.get('descricao')
        updated_estado = data.get('estado')


        query = "UPDATE Gaveta SET nome = %s, descricao = %s, estado = %s WHERE idGaveta = %s"
        values = (updated_name, updated_description, updated_estado, gaveta_id)

        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Gaveta updated successfully'}), 200

    except Exception as e:
        print('Error updating gaveta:', str(e))
        return jsonify({'message': 'Failed to update the gaveta'}), 500




# @app.route('/update_gaveta/<int:gaveta_id>', methods=['PUT'])
# def update_gaveta(gaveta_id):
#     print(f"Received PUT request for gaveta_id: {gaveta_id}")
#     try:
#         connection = mysql.connector.connect(**db_config)
#         cursor = connection.cursor()
#
#         # Check if the gaveta_id exists in the database
#         cursor.execute("SELECT idGaveta FROM Gaveta WHERE idGaveta = %s", (gaveta_id,))
#         result = cursor.fetchone()
#         if result is None:
#             cursor.close()
#             connection.close()
#             return jsonify({'message': 'Gaveta not found'}), 404
#
#         # Extract updated data from the request JSON
#         data = request.get_json()
#         updated_name = data.get('nome')
#         updated_description = data.get('descricao')
#         updated_estado = data.get('estado')
#
#         # Update the gaveta with the provided ID
#         query = "UPDATE Gaveta SET nome = %s, descricao = %s, estado = %s WHERE idGaveta = %s"
#         values = (updated_name, updated_description, updated_estado, gaveta_id)
#
#         cursor.execute(query, values)
#         connection.commit()
#         cursor.close()
#         connection.close()
#
#         return jsonify({'message': 'Gaveta updated successfully'}), 200
#
#     except Exception as e:
#         print('Error updating gaveta:', str(e))
#         return jsonify({'message': 'Failed to update the gaveta'}), 500
#

# Delete a gaveta by ID
# @app.route('/delete_gaveta/<int:gaveta_id>', methods=['DELETE'])
# def delete_gaveta(gaveta_id):
#     try:
#         connection = mysql.connector.connect(**db_config)
#         cursor = connection.cursor()
#
#         # Check if the gaveta_id exists in the database
#         cursor.execute("SELECT idGaveta FROM Gaveta WHERE idGaveta = %s", (gaveta_id,))
#         result = cursor.fetchone()
#         if result is None:
#             cursor.close()
#             connection.close()
#             return jsonify({'message': 'Gaveta not found'}), 404
#
#         # Delete the gaveta with the provided ID
#         query = "DELETE FROM Gaveta WHERE idGaveta = %s"
#         cursor.execute(query, (gaveta_id,))
#         connection.commit()
#         cursor.close()
#         connection.close()
#
#         return jsonify({'message': 'Gaveta deleted successfully'}), 200
#
#     except Exception as e:
#         print('Error deleting gaveta:', str(e))
#         return jsonify({'message': 'Failed to delete the gaveta'}), 500
#
#
#

# Delete a rack by ID
@app.route('/delete_rack/<int:rack_id>', methods=['DELETE'])
def delete_rack(rack_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check if the rack_id exists in the database
        cursor.execute("SELECT idRack FROM Rack WHERE idRack = %s", (rack_id,))
        result = cursor.fetchone()
        if result is None:
            cursor.close()
            connection.close()
            return jsonify({'message': 'Rack not found'}), 404

        # Delete the rack with the provided ID
        query = "DELETE FROM Rack WHERE idRack = %s"
        cursor.execute(query, (rack_id,))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'message': 'Rack deleted successfully'}), 200

    except Exception as e:
        print('Error deleting rack:', str(e))
        return jsonify({'message': 'Failed to delete the rack'}), 500



# Get all gavetas
@app.route('/get_gaveta', methods=['GET'])
def get_gavetas():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Gaveta"
        cursor.execute(query)
        gavetas = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify({'data': gavetas}), 200
    except Exception as e:
        print('Error fetching gavetas:', str(e))
        return jsonify({'message': 'Failed to fetch gavetas'}), 500


#drawerbyrack
@app.route('/get_gavetas_por_rack/<int:rack_id>', methods=['GET'])
def get_gavetas_por_rack(rack_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT G.* FROM Gaveta G INNER JOIN Rack R ON G.Rack_idRack = R.idRack WHERE R.idRack = %s"
        cursor.execute(query, (rack_id,))
        gavetas = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify({'data': gavetas}), 200
    except Exception as e:
        print('Error fetching gavetas:', str(e))
        return jsonify({'message': 'Failed to fetch gavetas'}), 500




@app.route('/get_racks', methods=['GET'])
def get_racks():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Rack"
        cursor.execute(query)
        racks = cursor.fetchall()
        cursor.close()
        connection.close()

        print('Racks retrieved successfully:', racks)

        return jsonify({'data': racks}), 200
    except Exception as e:
        print('Error fetching racks:', str(e))
        return jsonify({'message': 'Failed to fetch racks'}), 500

# Rota para criar um novo registro
# Rota para criar um novo registro
@app.route('/registro', methods=['POST'])
def create_registro():
    data = request.json
    print("Dados recebidos:", data)

    if data:
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Convertendo o valor da hora para o formato adequado (HH:MM:SS)
            hora_str = data['hora'].split('(')[1].split(')')[0]  # Extrair o valor da hora da string
            hora_parts = hora_str.split(':')  # Dividir a string em partes
            hora_str = f"{hora_parts[0]}:{hora_parts[1]}:00"  # Formatar a hora como HH:MM:SS

            print("Hora formatada:", hora_str)

            query = "INSERT INTO Registro (data, hora, cor, observacao, Gaveta_idGaveta) VALUES (%s, %s, %s, %s, %s)"
            values = (data['data'], hora_str, data['cor'], data['observacao'], data['Gaveta_idGaveta'])

            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'message': 'Registro criado com sucesso'}), 201
        except Exception as e:
            print("Erro ao inserir no banco de dados:", e)
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'Dados inválidos'}), 400

# Rota para atualizar um registro existente
@app.route('/registro/<int:idRegistro>', methods=['PUT'])
def update_registro(idRegistro):
    data = request.json
    if data:
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            query = "UPDATE Registro SET data = %s, hora = %s, cor = %s, observacao = %s, Gaveta_idGaveta = %s WHERE idRegistro = %s"
            values = (data['data'], data['hora'], data['cor'], data['observacao'], data['Gaveta_idGaveta'], idRegistro)
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()
            return jsonify({'message': 'Registro atualizado com sucesso'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'message': 'Dados inválidos'}), 400

# Rota para listar todos os registros
@app.route('/registro', methods=['GET'])
def list_registros():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Registro"
        cursor.execute(query)
        registros = cursor.fetchall()
        cursor.close()
        connection.close()
        return jsonify({'data': registros}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Rota para excluir um registro
@app.route('/registro/<int:idRegistro>', methods=['DELETE'])
def delete_registro(idRegistro):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        query = "DELETE FROM Registro WHERE idRegistro = %s"
        cursor.execute(query, (idRegistro,))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Registro excluído com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
