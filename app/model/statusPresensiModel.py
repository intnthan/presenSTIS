from app import db

class StatusPresensi(db.Model):
    __tablename__ = 'status_presensi'
    
    id_status = db.Column(db.Integer, 
                          primary_key=True, 
                          autoincrement=False)
    status = db.Column(db.String(50),
                       nullable=False)
    
    def __repr__(self):
        return '<StatusPresensi {}>'.format(self.id_status)