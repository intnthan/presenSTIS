from app import db

class Kelas(db.Model):
    __tablename__ = 'kelas'
    
    id_kelas = db.Column(db.Integer, 
                         primary_key=True,
                         autoincrement=True)
    nama_kelas = db.Column(db.String(5),
                           nullable=False)
    tahun_ajaran = db.Column(db.String(9),
                             nullable=False) 
    semester = db.Column(db.Integer,
                         nullable=False)   
    
    def __repr__(self):
        return '<Kelas {}>'.format(self.id_kelas)