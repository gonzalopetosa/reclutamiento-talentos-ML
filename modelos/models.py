from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Sequence


db = SQLAlchemy()

class CV(db.Model):
    __tablename__ = 'cv'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    frecuent_words = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<CV id={self.id} path={self.path}>'

    def to_dict(self):

        return {
            'id': self.id,
            'path': self.path,
            'text': self.text,
            'frecuent_words': self.frecuent_words
        }

class Candidato_apto(db.Model):

    __tablename__ = 'candidatos_aptos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.Text, nullable=False)
    apellido = db.Column(db.Text, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.Text, nullable=False)
    direccion = db.Column(db.Text, nullable=False)
    id_cv = db.Column(db.Integer, db.ForeignKey('cv.id') ,nullable=False)
    def __repr__(self):
        return f'<Candidato id={self.id} nombre={self.nombre} {self.apellido}>'

    def to_dict(self):

        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion,
            'id_cv': self.id_cv
        }

class Oferta(db.Model):

    __tablename__ = 'oferta'

    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    puesto = db.Column(db.Text, nullable=False)
    etiquetas = db.Column(db.Text)
    id_reclutador = db.Column(db.Integer, db.ForeignKey('reclutador.id'))



    def __repr__(self):
        return f'<oferta id={self.id} puesto={self.puesto}>'

    def to_dict(self):

        return {
            'id': self.id,
            'puesto': self.puesto,
            'etiquetas': self.etiquetas,
            'id_reclutador': self.id_reclutador
        }

class Reclutador(db.Model):

    __tablename__ = 'reclutador'

    # Columnas de la tabla
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    nombre = db.Column(db.Text , nullable=False)
    email = db.Column(db.Text, nullable=False)
    contraseña = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<reclutador id={self.id} nombre={self.nombre}>'

    def to_dict(self):

        return {
            'id': self.id,
            'nombre': self.nombre
        }

class Candidatos_oferta(db.Model):

    __tablename__ = 'candidatos_oferta'

    id = db.Column(db.Integer, Sequence('candidato_oferta'), primary_key=True)
    id_candidatoapto = db.Column(db.Integer, db.ForeignKey('candidato_apto.id') ,nullable=False)
    id_oferta = db.Column(db.Integer, db.ForeignKey('oferta.id') ,nullable=False)

    def __repr__(self):
        return f'<candidato_id={self.id_candidatoapto} oferta_id={self.id_oferta}>'

    def to_dict(self):

        return {
            'id': self.id,
            'id_candidatoapto': self.id_candidatoapto,
            'id_oferta': self.id_oferta
        }