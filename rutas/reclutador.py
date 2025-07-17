from flask import Blueprint, request, jsonify
from modelos.models import db, Reclutador

reclutador_bp = Blueprint('reclutador', __name__)

@reclutador_bp.route('/all', methods=['GET'])
def get_all():
    reclutadores = Reclutador.query.all()

    if not reclutadores:
        return jsonify({'Error':'LIST IS EMPY'})
    else:
        return jsonify([{
        'id':Reclutador.id,
        'nombre': Reclutador.nombre,
        'email': Reclutador.email
        } for Reclutador in reclutadores])


@reclutador_bp.route('/get/email', methods=['GET'])
def get_by_email():
    email = request.json['email']
    if not email:
        return jsonify({'error': 'Debe proporcionar un email'}), 400

    reclutador = Reclutador.query.filter_by(email=email).first()

    if reclutador:
        return jsonify({
            'id': reclutador.id,
            'nombre': reclutador.nombre,
            'email': reclutador.email
        })
    else:
        return jsonify({'error': 'No se encontró un reclutador con ese email'}), 404

@reclutador_bp.route('/add', methods=['POST'])
def add_reclutador():

    email = request.json['email']
    reclutador_existente = Reclutador.query.filter_by(email=email).first()

    if reclutador_existente:
        return jsonify({'Error':'The email to recruiter are used'}), 400

    try:
        new_reclutador = Reclutador(nombre = request.json['nombre'], email = request.json['email'])

        db.session.add(new_reclutador)
        db.session.commit()
        return jsonify({
            'id': new_reclutador.id,
            'nommbre': new_reclutador.nombre,
            'email': new_reclutador.email
        })
    except ValueError as e:
        db.session.rollback()
        return jsonify({'Error': str(e)})

@reclutador_bp.route('/modify', methods=['PUT'])
def modify():
    data = request.get_json()
    id = data.get('id')
    nombre = data.get('nombre')
    email = data.get('email')

    if not id or not nombre or not email:
        return jsonify({'error': 'Todos los campos deben estar completo'}), 400

    reclutador_existente = Reclutador.query.filter_by(email=email).first()

    if reclutador_existente:
        return jsonify({'Error':'El campo email ya esta ocupado'}), 400

    reclutador_db = Reclutador.query.get(id)

    if not reclutador_db:
        return jsonify({'Error':'No existe reclutador indicado'}), 404
    try:
        reclutador_db.nombre = nombre
        reclutador_db.email = email
        db.session.commit()
        return jsonify({'Data':'Se actualizo reclutador'}), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify({'Error': str(e)})


@reclutador_bp.route('/delete/id', methods=['DELETE'])
def delete_by_id():
    data = request.get_json()
    id = data.get('id')

    if not id:
        return jsonify({'Error': 'El campo "id" es obligatorio'}), 400

    reclutador_db = Reclutador.query.get(request.json['id'])

    if not reclutador_db:
        return jsonify({'Error':'The recruiter not exists'}), 404

    try:
        db.session.delete(reclutador_db)
        db.session.commit()
        return jsonify({'data':'se elimino al reclutador'}), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify({'Error': str(e)})
















