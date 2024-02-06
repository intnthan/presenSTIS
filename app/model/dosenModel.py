from app import db

class Dosen(db.Model):
    
    __tablename__ = 'dosen'
    
    nip = db.Column(db.String(25),
                    primary_key=True, 
                    autoincrement=False)
    nama_dosen = db.Column(db.String(256),
                            nullable=False)
    
    def __repr__(self) :
        return '<Dosen {}>'.format(self.nip)