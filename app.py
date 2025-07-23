from flask import request, Flask, jsonify, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from modelos.models import db
from flask_cors import CORS
from rutas.oferta import oferta_bp
from rutas.reclutador import reclutador_bp
from rutas.candidato_apto import candidato_apto_bp
from rutas.auth import auth_bp
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('JWT_SECRET')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'

db.init_app(app)
CORS(app, supports_credentials=True)

app.register_blueprint(oferta_bp, url_prefix='/oferta')
app.register_blueprint(reclutador_bp, url_prefix='/reclutador')
app.register_blueprint(candidato_apto_bp, url_prefix='/candidatos_aptos')
app.register_blueprint(auth_bp, url_prefix="/auth")

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('token')
    print(token)
    if not token:
        return redirect(url_for('index'))
    return render_template('index.html')

if __name__== '__main__':
    app.run(port=int(os.environ.get("FLASK_PORT", 5000)))
