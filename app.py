from flask import request, Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from modelos.models import db
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/RECLUTACION'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

from rutas.oferta import oferta_bp
from rutas.reclutador import reclutador_bp
from rutas.candidato_apto import candidato_apto_bp

app.register_blueprint(oferta_bp, url_prefix='/oferta')
app.register_blueprint(reclutador_bp, url_prefix='/reclutador')
app.register_blueprint(candidato_apto_bp, url_prefix='/candidatos_aptos')

if __name__== '__main__':
    app.run(port=int(os.environ.get("FLASK_PORT", 5000)))
