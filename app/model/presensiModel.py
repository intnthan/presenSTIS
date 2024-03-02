from app import db
from datetime import datetime
from app.model.mahasiswaModel import Mahasiswa
from app.model.perkuliahanModel import Perkuliahan
from app.model.statusPresensiModel import StatusPresensi

class Presensi(db.Model):
        
        __tablename__ = 'presensi'
        
        id_presensi = db.Column(db.Integer, 
                            primary_key=True, 
                            autoincrement=True)
        nim = db.Column(db.String(9),
                        db.ForeignKey(Mahasiswa.nim,
                                        ondelete='CASCADE'),
                        nullable=False)
        id_perkuliahan = db.Column(db.Integer,
                                db.ForeignKey(Perkuliahan.id_perkuliahan, 
                                                ondelete='CASCADE'),
                                nullable=False)
        
        # waktu nya sementara dibikin default aja, nanti diubah sesuai keadaan absen
        waktu = db.Column(db.Time,
                        nullable=False, 
                        default=datetime.now().time().strftime('%H:%M:%S'))
        id_status = db.Column(db.Integer,
                           db.ForeignKey(StatusPresensi.id_status,
                                         ondelete='CASCADE'),
                        nullable=False)
        
        perkuliahan = db.relationship('Perkuliahan', backref=db.backref('presensi', lazy=True))
        mahasiswa = db.relationship('Mahasiswa', backref=db.backref('presensi', lazy=True))
        status_presensi = db.relationship('StatusPresensi', backref=db.backref('presensi', lazy=True))
        
        def __repr__(self):
            return '<Presensi {}>'.format(self.id_presensi)