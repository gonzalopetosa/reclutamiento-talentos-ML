from flask import Blueprint, request, jsonify
from modelos.models import db, Reclutador
import hashlib
from services.Security import Security

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/reclutador/login', methods=['POST'])
def reclutador_login():
    data = request.get_json()
    email = data.get('email')
    contraseña = data.get('contraseña')

    if not email or not contraseña:
        return jsonify({'Error':'Los compos no estan completos'}), 401

    reclutador_existente = Reclutador.query.filter_by(email=email).first()
    hash_password = hashlib.sha256(contraseña.encode('utf-8')).hexdigest()

    if not reclutador_existente:
        return jsonify({'error':'Credencial incorrecta'}), 401

    if hash_password == reclutador_existente.contraseña:
        try:
            token = Security.generate_token(reclutador_existente)
            return jsonify({
                    'id_reclutador':reclutador_existente.id,
                    'Token': token}), 200
        except ValueError as e:
            return jsonify({'Error': str(e) }), 401
    else:
        return jsonify({'error':'Credencial incorrecta'}), 401





