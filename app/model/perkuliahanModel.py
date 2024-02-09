from app import db 
from app.model.kelasModel import Kelas
from app.model.mataKuliahModel import MataKuliah
# from app.model.statusPerkuliahanModel import StatusPerkuliahan

class Perkuliahan(db.Model):
    
    __tablename__ = 'perkuliahan'
    
    id_perkuliahan = db.Column(db.Integer, 
                               primary_key=True, 
                               autoincrement=True)
    id_kelas = db.Column(db.Integer,
                         db.ForeignKey(Kelas.id_kelas, 
                                       ondelete='CASCADE'),
                         nullable=False)
    id_mk = db.Column(db.Integer,
                      db.ForeignKey(MataKuliah.id_mk, 
                                    ondelete='CASCADE'),
                      nullable=False)
    pertemuan = db.Column(db.Integer,
                          nullable=False)
    jam_mulai = db.Column(db.Time,
                          nullable=False)
    jam_selesai = db.Column(db.Time,
                          nullable=False)
    tanggal = db.Column(db.Date,
                        nullable=False)
    ruangan = db.Column(db.Integer,
                        nullable=False)
    # id_status_perkuliahan = db.Column(db.Integer,
    #                                   db.ForeignKey(StatusPerkuliahan.id_status_perkuliahan, 
    #                                                 ondelete='CASCADE'),
    #                                   nullable=False)
    
    kelas = db.relationship('Kelas', backref=db.backref('perkuliahan', lazy=True))
    mata_kuliah = db.relationship('MataKuliah', backref=db.backref('perkuliahan', lazy=True))
    # status_perkuliahan = db.relationship('StatusPerkuliahan', backref=db.backref('perkuliahan', lazy=True))
    
    def __repr__(self):
        return '<Perkuliahan {}>'.format(self.id_perkuliahan)