from app import db

from app.model.akunModel import Akun

class Dosen(db.Model):
    
    __tablename__ = 'dosen'
    
    nip = db.Column(db.String(25),
                    primary_key=True, 
                    autoincrement=False)
    username = db.Column(db.String(256),
                         db.ForeignKey(Akun.username,
                                        ondelete='CASCADE'),
                         nullable=False)
    nama_dosen = db.Column(db.String(256),
                            nullable=False)
    
    akun = db.relationship('Akun', backref=db.backref('dosen', lazy=True))
    
    def __repr__(self) :
        return '<Dosen {}>'.format(self.nip)