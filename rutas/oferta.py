from flask import Blueprint, request, jsonify
from modelos.models import db, Oferta

oferta_bp = Blueprint('oferta', __name__)

@oferta_bp.route('/')
def obtener_ofertar():
    ofertas = Oferta.query.all()
    return jsonify([{
    'id':Oferta.id,
    'puesto':Oferta.puesto,
    'etiquetas':Oferta.etiquetas
    } for Oferta in ofertas])

@oferta_bp.route('/add', methods=['POST'])
def add_oferta():
    nueva_oferta = Oferta(puesto = request.json['puesto'], etiquetas = request.json['etiquetas'], id_reclutador = request.json['id_reclutador'])
    db.session.add(nueva_oferta)
    db.session.commit()
    return jsonify(
    {'puesto': Oferta.puesto}
    )
