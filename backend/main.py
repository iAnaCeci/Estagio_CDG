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
        return True
    except Exception as e:
        print('Error inserting drawer information:', str(e))
        return False
    finally:
        cursor.close()
        connection.close()

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
        return rack_id
    except Exception as e:
        print('Error inserting rack information:', str(e))
        return None
    finally:
        cursor.close()
        connection.close()

@app.route('/add_rack', methods=['POST'])
def add_rack():
    data = request.get_json()
    if 'nome' in data and 'localizacao' in data and 'descricao' in data:
        nome = data['nome']
        localizacao = data['localizacao']
        descricao = data['descricao']
        rack_id = insert_rack(nome, localizacao, descricao)
        if rack_id is not None:
            gaveta_data = data.get('gavetas', [])
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

@app.route('/add_drawer', methods=['POST'])
def add_drawer():
    data = request.get_json()
    if 'nome' in data and 'descricao' in data and 'estado' in data and 'Rack_idRack' in data:
        nome = data['nome']
        descricao = data['descricao']
        estado = data['estado']
        rack_id = data['Rack_idRack']
        if insert_drawer(nome, descricao, estado, rack_id):
            return jsonify({'message': 'Drawer added successfully'}), 201
        else:
            return jsonify({'message': 'Failed to add the drawer'}), 500
    else:
        return jsonify({'message': 'Invalid data'}), 400

# @app.route('/update_gaveta', methods=['PUT'])
# def update_gaveta():
#     data = request.get_json()
#     if 'id' in data and 'nome' in data and 'descricao' in data and 'estado' in data:
#         gaveta_id = data['id']
#         updated_name = data['nome']
#         updated_description = data['descricao']
#         updated_estado = data['estado']
#         try:
#             connection = mysql.connector.connect(**db_config)
#             cursor = connection.cursor()
#             query = "UPDATE Gaveta SET nome = %s, descricao = %s, estado = %s WHERE idGaveta = %s"
#             values = (updated_name, updated_description, updated_estado, gaveta_id)
#             cursor.execute(query, values)
#             connection.commit()
#             return jsonify({'message': 'Gaveta updated successfully'}), 200
#         except Exception as e:
#             print('Error updating gaveta:', str(e))
#             return jsonify({'message': 'Failed to update the gaveta'}), 500
#         finally:
#             cursor.close()
#             connection.close()
#     else:
#         return jsonify({'message': 'Invalid data'}), 400

@app.route('/update_gaveta', methods=['PUT'])
def update_gaveta():
    data = request.get_json()
    if 'id' in data and 'nome' in data and 'descricao' in data and 'estado' in data:
        gaveta_id = data['id']
        updated_name = data['nome']
        updated_description = data['descricao']
        updated_estado = data['estado']
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Buscar o estado atual
            cursor.execute("SELECT estado FROM Gaveta WHERE idGaveta = %s", (gaveta_id,))
            current_state = cursor.fetchone()
            if current_state:
                estado_anterior = current_state[0]
            else:
                return jsonify({'message': 'Gaveta não encontrada'}), 404

            # Atualizar a gaveta com o novo estado
            query = "UPDATE Gaveta SET nome = %s, descricao = %s, estado = %s WHERE idGaveta = %s"
            values = (updated_name, updated_description, updated_estado, gaveta_id)
            cursor.execute(query, values)
            connection.commit()

            return jsonify({'message': 'Gaveta atualizada com sucesso', 'estado_anterior': estado_anterior}), 200
        except Exception as e:
            print('Erro ao atualizar a gaveta:', str(e))
            return jsonify({'message': 'Falha ao atualizar a gaveta'}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({'message': 'Dados inválidos'}), 400


@app.route('/rack_details/<int:rack_id>', methods=['GET'])
def rack_details(rack_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Rack WHERE idRack = %s"
        cursor.execute(query, (rack_id,))
        rack = cursor.fetchone()
        if rack:
            return jsonify({'rack': rack}), 200
        else:
            return jsonify({'message': 'Rack not found'}), 404
    except Exception as e:
        print('Error fetching rack details:', str(e))
        return jsonify({'message': 'Failed to fetch rack details'}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_gaveta/<int:gaveta_id>', methods=['DELETE'])
def delete_gaveta(gaveta_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT idGaveta FROM Gaveta WHERE idGaveta = %s", (gaveta_id,))
        result = cursor.fetchone()
        if result is None:
            return jsonify({'message': 'Gaveta not found'}), 404
        cursor.execute("DELETE FROM Gaveta WHERE idGaveta = %s", (gaveta_id,))
        connection.commit()
        return jsonify({'message': 'Gaveta deleted successfully'}), 200
    except Exception as e:
        print('Error deleting gaveta:', str(e))
        return jsonify({'message': 'Failed to delete the gaveta'}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/delete_rack/<int:rack_id>', methods=['DELETE'])
def delete_rack(rack_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Registro WHERE Gaveta_idGaveta IN (SELECT idGaveta FROM Gaveta WHERE Rack_idRack = %s)", (rack_id,))
        cursor.execute("DELETE FROM Gaveta WHERE Rack_idRack = %s", (rack_id,))
        cursor.execute("DELETE FROM Rack WHERE idRack = %s", (rack_id,))
        connection.commit()
        return jsonify({'message': 'Rack and associated gavetas and registros deleted successfully'}), 200
    except Exception as e:
        print('Error deleting rack:', str(e))
        return jsonify({'message': 'Failed to delete the rack'}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_gaveta', methods=['GET'])
def get_gavetas():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Gaveta"
        cursor.execute(query)
        gavetas = cursor.fetchall()
        return jsonify({'data': gavetas}), 200
    except Exception as e:
        print('Error fetching gavetas:', str(e))
        return jsonify({'message': 'Failed to fetch gavetas'}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_gavetas_por_rack/<int:rack_id>', methods=['GET'])
def get_gavetas_por_rack(rack_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT G.* FROM Gaveta G INNER JOIN Rack R ON G.Rack_idRack = R.idRack WHERE R.idRack = %s"
        cursor.execute(query, (rack_id,))
        gavetas = cursor.fetchall()
        return jsonify({'data': gavetas}), 200
    except Exception as e:
        print('Error fetching gavetas:', str(e))
        return jsonify({'message': 'Failed to fetch gavetas'}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_racks', methods=['GET'])
def get_racks():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT idRack, nome, localizacao, descricao FROM Rack"
        cursor.execute(query)
        racks = cursor.fetchall()
        return jsonify({'data': racks}), 200
    except Exception as e:
        print('Error fetching racks:', str(e))
        return jsonify({'message': 'Failed to fetch racks'}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/registro', methods=['POST'])
def create_registro():
    data = request.json
    if data:
        try:
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()
            hora_str = data['hora'].split('(')[1].split(')')[0]
            hora_parts = hora_str.split(':')
            hora_str = f"{hora_parts[0]}:{hora_parts[1]}:00"
            query = "INSERT INTO Registro (data, hora, cor, observacao, Gaveta_idGaveta) VALUES (%s, %s, %s, %s, %s)"
            values = (data['data'], hora_str, data['cor'], data['observacao'], data['Gaveta_idGaveta'])
            cursor.execute(query, values)
            connection.commit()
            return jsonify({'message': 'Registro criado com sucesso'}), 201
        except Exception as e:
            print("Erro ao inserir no banco de dados:", e)
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    else:
        return jsonify({'message': 'Dados inválidos'}), 400

@app.route('/registro', methods=['GET'])
def list_registros():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Registro"
        cursor.execute(query)
        registros = cursor.fetchall()
        return jsonify({'data': registros}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/registro/<int:registro_id>', methods=['DELETE'])
def delete_registro(registro_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Registro WHERE idRegistro = %s", (registro_id,))
        registro = cursor.fetchone()
        if not registro:
            return jsonify({'message': 'Registro não encontrado'}), 404
        cursor.execute("DELETE FROM Registro WHERE idRegistro = %s", (registro_id,))
        connection.commit()
        return jsonify({'message': 'Registro excluído com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/get_registros_por_gaveta_data/<int:gaveta_id>/<string:data>', methods=['GET'])
def get_registros_por_gaveta_data(gaveta_id, data):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = "SELECT cor, observacao FROM Registro WHERE Gaveta_idGaveta = %s AND data = %s"
        cursor.execute(query, (gaveta_id, data))
        registros = cursor.fetchall()
        if registros:
            return jsonify({'data': registros}), 200
        else:
            return jsonify({'message': 'Nenhum registro encontrado para a gaveta e data especificadas'}), 404
    except mysql.connector.Error as err:
        print('Erro ao buscar registros:', err)
        return jsonify({'message': 'Erro ao buscar registros'}), 500
    finally:
        cursor.close()
        connection.close()


@app.route('/rack_estado_anterior/<int:rack_id>', methods=['GET'])
def rack_estado_anterior(rack_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        # Query para obter o estado mais recente antes da data atual para todas as gavetas associadas ao rack
        query = """
            SELECT G.idGaveta, R.estado, R.cor, R.observacao
            FROM Registro R
            INNER JOIN Gaveta G ON R.Gaveta_idGaveta = G.idGaveta
            WHERE G.Rack_idRack = %s
            ORDER BY R.data DESC, R.hora DESC
        """
        cursor.execute(query, (rack_id,))
        registros = cursor.fetchall()
        if registros:
            # Agrupar registros por gaveta e pegar o mais recente para cada gaveta
            gavetas = {}
            for registro in registros:
                gaveta_id = registro['idGaveta']
                if gaveta_id not in gavetas:
                    gavetas[gaveta_id] = registro
            return jsonify({'estado_anterior_rack': list(gavetas.values())}), 200
        else:
            return jsonify({'message': 'Nenhum estado anterior encontrado para o rack'}), 404
    except Exception as e:
        print('Erro ao buscar o estado anterior do rack:', str(e))
        return jsonify({'message': 'Falha ao buscar o estado anterior do rack'}), 500
    finally:
        cursor.close()
        connection.close()





@app.route('/get_registros_anteriores_por_rack_data/<int:rackId>/<string:formattedDate>', methods=['GET'])
def get_registros_anteriores_por_rack_data(rackId, formattedDate):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT R.*
            FROM Registro R
            INNER JOIN Gaveta G ON R.Gaveta_idGaveta = G.idGaveta
            WHERE G.Rack_idRack = %s AND R.data <= %s
                AND R.cor = %s AND R.observacao = %s
            ORDER BY R.data DESC
        """

        cor = request.args.get('cor')
        observacao = request.args.get('observacao')

        cursor.execute(query, (rackId, formattedDate, cor, observacao))
        registros = cursor.fetchall()
        return jsonify({'data': registros}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()




if __name__ == '__main__':
    app.run(debug=True)
