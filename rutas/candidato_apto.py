from flask import Blueprint, request, jsonify
from modelos.models import db, Candidato_apto, CV

candidato_apto_bp = Blueprint('candidatos_aptos', __name__)

@candidato_apto_bp.route('/all', methods=['GET'])
def obtener_candidatos():
    candidatos = Candidato_apto.query.all()
    return jsonify([{
        'id': candidato.id,
        'nombre': candidato.nombre,
        'apellido': candidato.apellido,
        'telefono': candidato.telefono,
        'email': candidato.email,
        'direccion': candidato.direccion,
        'id_cv': candidato.id_cv
    } for candidato in candidatos])

@candidato_apto_bp.route('/get/<int:id>', methods=['GET'])
def get_by_id(id):

    if not id:
        return jsonify({'Error': 'Debes proporcionar un ID'}), 400

    candidato_db = Candidato_apto.query.get(id)

    if not candidato_db:
        return jsonify({'Error': 'No existe el candidato'}), 404

    return jsonify({
        'nombre': candidato_db.nombre,
        'apellido': candidato_db.apellido,
        'telefono': candidato_db.telefono,
        'email': candidato_db.email,
        'direccion': candidato_db.direccion,
        'id_cv': candidato_db.id_cv
    }), 200

@candidato_apto_bp.route('/add', methods=['POST'])
def add_candidato():
    data = request.get_json()
    id_cv = data.get('id_cv')

    if not id_cv:
        return jsonify({'Error': 'El campo id_cv es obligatorio'}), 400

    cv_db = CV.query.get(id_cv)

    if not cv_db:
        return jsonify({'Error': 'No existe el CV especificado'}), 404

    # Validar campos obligatorios
    campos_obligatorios = ['nombre', 'apellido', 'telefono', 'email', 'direccion']
    if not all(campo in data for campo in campos_obligatorios):
        return jsonify({'Error': 'Faltan campos obligatorios'}), 400

    try:
        nuevo_candidato = Candidato_apto(
            nombre=data['nombre'],
            apellido=data['apellido'],
            telefono=data['telefono'],
            email=data['email'],
            direccion=data['direccion'],
            id_cv=id_cv
        )

        db.session.add(nuevo_candidato)
        db.session.commit()

        return jsonify({
            'id': nuevo_candidato.id,
            'nombre': nuevo_candidato.nombre,
            'apellido': nuevo_candidato.apellido,
            'email': nuevo_candidato.email
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)}), 500

@candidato_apto_bp.route('/modify/<int:id>', methods=['PUT'])
def modify(id):
    if not id:
        return jsonify({'Error': 'Debes proporcionar un ID'}), 400

    candidato_db = Candidato_apto.query.get(id)
    if not candidato_db:
        return jsonify({'Error': 'No existe el candidato'}), 404

    data = request.get_json()

    # Validar existencia del CV si se quiere modificar
    if 'id_cv' in data:
        cv_db = CV.query.get(data['id_cv'])
        if not cv_db:
            return jsonify({'Error': 'No existe el CV especificado'}), 404

    try:
        candidato_db.nombre = data.get('nombre', candidato_db.nombre)
        candidato_db.apellido = data.get('apellido', candidato_db.apellido)
        candidato_db.telefono = data.get('telefono', candidato_db.telefono)
        candidato_db.email = data.get('email', candidato_db.email)
        candidato_db.direccion = data.get('direccion', candidato_db.direccion)
        candidato_db.id_cv = data.get('id_cv', candidato_db.id_cv)

        db.session.commit()
        return jsonify({
            'id': candidato_db.id,
            'nombre': candidato_db.nombre,
            'apellido': candidato_db.apellido,
            'email': candidato_db.email
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)}), 500

@candidato_apto_bp.route('/delete/<int:id>', methods=['DELETE'])
def delete_by_id(id):
    if not id:
        return jsonify({'Error': 'Debes proporcionar un ID'}), 400

    candidato_db = Candidato_apto.query.get(id)
    if not candidato_db:
        return jsonify({'Error': 'No existe el candidato'}), 404

    try:
        db.session.delete(candidato_db)
        db.session.commit()
        return jsonify({'Mensaje': 'Candidato eliminado correctamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error': str(e)}), 500
