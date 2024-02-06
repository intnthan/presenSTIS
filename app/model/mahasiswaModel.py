from app import db
from app.model.kelasModel import Kelas

class Mahasiswa(db.Model):
    __tablename__ = 'mahasiswa'
    
    nim = db.Column(db.String(9),
                    primary_key=True, 
                    autoincrement=False)
    nama_mhs = db.Column(db.String(256),
                         nullable=False)
    id_kelas = db.Column(db.Integer,
                         db.ForeignKey(Kelas.id_kelas),
                         nullable=False)
    embeddings = db.Column(db.Text,
                           nullable=True)
    kelas = db.relationship('Kelas', backref=db.backref('mahasiswa', lazy=True))
    
    def __repr__(self):
       return '<Mahasiswa {}>'.format(self.nim)
    