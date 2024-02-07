from app import db 

class StatusPerkuliahan(db.Model):
        
        __tablename__ = 'status_perkuliahan'
        
        id_status_perkuliahan = db.Column(db.Integer, 
                                        primary_key=True)
        status_perkuliahan = db.Column(db.String(30),
                                       nullable=False)
        
        def __repr__(self):
            return '<StatusPerkuliahan {}>'.format(self.id_status_perkuliahan)