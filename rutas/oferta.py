from flask import Blueprint, request, jsonify
from modelos.models import db, Oferta, Reclutador
from services.Security import Security
from services.decorador import token_required


oferta_bp = Blueprint('oferta', __name__)

@oferta_bp.route('/all')
@token_required
def obtener_ofertar():
    ofertas = Oferta.query.all()
    return jsonify([{
        'id':Oferta.id,
        'puesto':Oferta.puesto,
        'etiquetas':Oferta.etiquetas,
        'reclutador':Oferta.id_reclutador
    } for Oferta in ofertas]) , 200

@oferta_bp.route('/get/<int:id>')
@token_required
def get_by_id(id):

    oferta_db = Oferta.query.get_or_404(id)

    return jsonify({
        'puesto': oferta_db.puesto,
        'etiquetas': oferta_db.etiquetas,
        'id_reclutador': oferta_db.id_reclutador
    }), 200


@oferta_bp.route('/add', methods=['POST'])
@token_required
def add_oferta():

    data = request.get_json()
    id_reclutador = data.get('id_reclutador')
    puesto = data.get('puesto')
    etiquetas = data.get('etiquetas')

    if not id_reclutador or not puesto or not etiquetas:
        return jsonify({
        'Error':'Peticion incompleta'
        }) , 400

    reclutador_db = Reclutador.query.get(id_reclutador)

    if not reclutador_db:
        return jsonify({
        'Error':'No existe reclutador'
        }) , 404

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
@token_required
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
@token_required
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
















