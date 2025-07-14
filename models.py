from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CV(db.model):
    __tablename__ = 'cv'

    id = db.Column(db.Integer, Sequence('cv_id_seq'), primary_key=True)
    path = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False)
    frecuent_words = db.Column(db.Text, nullable=False)
    #FOREIGN KEY RELACION ENTRE CV--CANDIDATOS_APTO
    id_candidato = db.Column(db.Integer, db.ForeignKey('candidato.id') ,nullable=False)

    def __repr__(self):
        return f'<CV id={self.id} candidate={self.id_candidato} path={self.path}>'

    def to_dict(self):

        return {
            'id': self.id,
            'path': self.path,
            'text': self.text,
            'frecuent_words': self.frecuent_words,
            'id_candidato': self.id_candidato
        }

class Candidato_apto(db.Model):

    __tablename__ = 'candidato_apto'

    id = db.Column(db.Integer, Sequence('candidato_apto_id_seq'), primary_key=True)
    nombre = db.Column(db.Text, nullable=False)
    apellido = db.Column(db.Text, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.Text, nullable=False)
    direccion = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Candidato id={self.id} nombre={self.nombre} {self.apellido}>'

    def to_dict(self):

        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'telefono': self.telefono,
            'email': self.email,
            'direccion': self.direccion
        }

class Oferta(db.Model):

    __tablename__ = 'oferta'

    id = db.Column(db.Integer, Sequence('oferta_id_seq'), primary_key=True)
    puesto = db.Column(db.String(12), nullable=False)
    etiquetas = db.Column(db.Text)
    id_reclutador = db.Column(db.Integer, db.ForeignKey('reclutador.id'))
    id_candidato_apto = db.Column(db.Integer, db.ForeignKey('candidato_apto.id'))


    def __repr__(self):
        return f'<JobPosition id={self.id} puesto={self.puesto}>'

    def to_dict(self):

        return {
            'id': self.id,
            'puesto': self.puesto,
            'etiquetas': self.etiquetas,
            'id_reclutador': self.id_reclutador,
            'id_candidato_apto': self.id_candidato_apto
        }

class Reclutador(db.Model):

    __tablename__ = 'reclutador'

    # Columnas de la tabla
    id = db.Column(db.Integer, Sequence('reclutador'), primary_key=True)
    nombre = db.Column(db.String(12), nullable=False)
    oferta = db.Column(db.Integer, db.ForeignKey('oferta.id'))

    def __repr__(self):
        return f'<Recruiter id={self.id} nombre={self.nombre}>'

    def to_dict(self):

        return {
            'id': self.id,
            'nombre': self.nombre,
            'oferta': self.oferta
        }