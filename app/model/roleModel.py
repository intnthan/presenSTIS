from app import db

class Role(db.Model):
    
    __tablename__ = 'role'
    id_role = db.Column(db.Integer, 
                        primary_key=True)
    nama_role = db.Column(db.String(30), 
                          nullable=False)
    deskripsi = db.Column(db.String(256), 
                          nullable=True)
    
    def __repr__(self):
        return '<Role {}>'.format(self.id_role) 