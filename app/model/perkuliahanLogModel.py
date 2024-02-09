from app import db 

from app.model.perkuliahanModel import Perkuliahan
from app.model.statusPerkuliahanModel import StatusPerkuliahan

class PerkuliahanLog(db.Model):
    
    __tablename__ = 'perkuliahan_log'   
    
    id_perkuliahan_log = db.Column(db.Integer,
                            primary_key=True)
    id_perkuliahan = db.Column(db.Integer,
                            db.ForeignKey(Perkuliahan.id_perkuliahan),
                            nullable=False)
    id_status_perkuliahan = db.Column(db.Integer,
                            db.ForeignKey(StatusPerkuliahan.id_status_perkuliahan),
                            nullable=False)
    jam = db.Column(db.Time,
                    nullable=True)
    
    
    perkuliahan = db.relationship('Perkuliahan', backref=db.backref('perkuliahan_log', lazy=True))
    status_perkuliahan = db.relationship('StatusPerkuliahan', backref=db.backref('perkuliahan_log', lazy=True))
    
    def __repr__(self):
        return '<PerkuliahanLog {}>'.format(self.id_perkuliahan_log)