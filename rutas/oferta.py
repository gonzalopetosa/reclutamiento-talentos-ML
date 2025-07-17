from flask import Blueprint, request, jsonify
from modelos.models import db, Oferta, Reclutador

oferta_bp = Blueprint('oferta', __name__)

@oferta_bp.route('/all')
def obtener_ofertar():

    ofertas = Oferta.query.all()

    return jsonify([{
        'id':Oferta.id,
        'puesto':Oferta.puesto,
        'etiquetas':Oferta.etiquetas
    } for Oferta in ofertas])

@oferta_bp.route('/get/id')
def get_by_id():
    data = request.get_json()
    id_oferta = data.get('id')

    if not id_oferta:
        return jsonify({
        'Error':'El campo id no fue completado'
        }) , 400

    oferta_db = Oferta.query.get(id_oferta)

    if not oferta_db:
        return jsonify({
        'Error':'No existe oferta'
        }) , 404
    else:
        return jsonify({
            'puesto': oferta_db.puesto,
            'etiquetas': oferta_db.etiquetas,
            'reclurado_asociado': oferta_db.id_reclutador
        }), 200


@oferta_bp.route('/add', methods=['POST'])
def add_oferta():

    data = request.get_json()
    id_reclutador = data.get('id_reclutador')

    if not id_reclutador:
        return jsonify({
        'Error':'El campo id_reclutador no fue completado'
        }) , 400

    reclutador_db = Reclutador.query.get(id_reclutador)

    if not reclutador_db:
        return jsonify({
        'Error':'No existe reclutador'
        }) , 404

    puesto = data.get('puesto')
    etiquetas = data.get('etiquetas')

    if not puesto or not etiquetas:
        return jsonify({'Error': 'Los campos "puesto" y "etiquetas" son obligatorios'}), 400

    try:
        nueva_oferta = Oferta(
            puesto = puesto,
            etiquetas = etiquetas,
            id_reclutador = id_reclutador)

        db.session.add(nueva_oferta)
        db.session.commit()
        return jsonify({
            'puesto': nueva_oferta.puesto,
            'etiquetas': nueva_oferta.etiquetas,
            'reclurado_asociado': nueva_oferta.id_reclutador
        }), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify( {'Error': str(e) }), 400

@oferta_bp.route('/modify', methods=['PUT'])
def modify():
    data = request.get_json()

    id_oferta_db = data.get('id')
    id_reclutador_db = data.get('id_reclutador')
    puesto = data.get('puesto')
    etiquetas = data.get('etiquetas')

    if not id_reclutador_db or not puesto or not etiquetas or not id_oferta_db:
        return jsonify({'Error': 'Uno de los campos no estan completos'}), 400

    oferta_db = Oferta.query.get(id_oferta_db)
    if not oferta_db:
        return jsonify({
        'Error':'No existe oferta'
        }) , 404

    reclutador_db = Reclutador.query.get(id_reclutador_db)
    if not reclutador_db:
        return jsonify({
        'Error':'No existe reclutador'
        }) , 404

    try:
        oferta_db.puesto = puesto
        oferta_db.etiquetas = etiquetas
        oferta_db.id_reclutador = id_reclutador_db
        db.session.commit()
        return jsonify({
            'id':oferta_db.id,
            'puesto': oferta_db.puesto,
            'etiquetas': oferta_db.etiquetas,
            'reclurado_asociado': oferta_db.id_reclutador
        }), 201
    except ValueError as e:
        db.session.rollback()
        return jsonify( {'Error': str(e) }), 400

@oferta_bp.route('/delete/id', methods=['DELETE'])
def delete_by_id():
    data = request.get_json()
    id = data.get('id')

    if not id:
        return jsonify({'Error': 'Debes ingresar el campo ID'}), 400

    oferta_db = Oferta.query.get(id)

    if not oferta_db:
        return jsonify({
        'Error':'No existe oferta'
        }) , 404

    try:
        db.session.delete(oferta_db)
        db.session.commit()
        return jsonify({'data':'se elimino al reclutador'}), 200
    except ValueError as e:
        db.session.rollback()
        return jsonify( {'Error': str(e) }), 400
















