from flask import Blueprint, request, jsonify, session
from modelos.models import db, Reclutador
import hashlib
from services.Security import Security


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/reclutador/login', methods=['POST'])
def reclutador_login():
    data = request.get_json(force=True)
    email = data.get('email')
    contraseña = data.get('contraseña')

    if not email or not contraseña:
        return jsonify({'Error':'Los compos no estan completos'}), 401

    reclutador_existente = Reclutador.query.filter_by(email=email).first()
    hash_password = hashlib.sha256(contraseña.encode('utf-8')).hexdigest()

    if not reclutador_existente or hash_password != reclutador_existente.contraseña:
        return jsonify({'error':'Credencial incorrecta'}), 401

    try:
        token = Security.generate_token(reclutador_existente)

        response = jsonify({
            'success': True,
            'reclutador_id': reclutador_existente.id,
            'reclutador_nombre': reclutador_existente.nombre
        })

        response.set_cookie(
            'token',
            token,
            max_age=Security.expiration_time,
            httponly=False,
            secure=False,
            samesite='Lax'
        )
        response.set_cookie('reclutador_id', str(reclutador_existente.id), httponly=False)
        response.set_cookie('reclutador_nombre', reclutador_existente.nombre, httponly=False)
        response.set_cookie('reclutador_email', reclutador_existente.email, httponly=False)

        return response, 200

    except ValueError as e:
        return jsonify({'Error': str(e) }), 401





