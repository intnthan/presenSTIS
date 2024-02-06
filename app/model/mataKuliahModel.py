from app import db 

from app.model.dosenModel import Dosen

class MataKuliah(db.Model):
    
    __tablename__ = 'mata_kuliah'
    
    id_mk = db.Column(db.Integer, 
                      primary_key=True, 
                      autoincrement=True)
    kode_mk = db.Column(db.String(7), 
                        nullable=False)
    nama_mk = db.Column(db.String(256),
                        nullable=False)
    nip = db.Column(db.String(25),
                    db.ForeignKey(Dosen.nip),
                    nullable=False)
    jumlah_pertemuan = db.Column(db.Integer,
                                 nullable=False)
    
    dosen = db.relationship('Dosen', backref=db.backref('mata_kuliah', lazy=True))
    
    def __repr__(self):
        return '<MataKuliah {}>'.format(self.id_mk)