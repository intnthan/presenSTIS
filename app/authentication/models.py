from flask_login import UserMixin
from app import db, login_manager
from app.authentication.util import hash_pass

class Role(db.Model):
    id_role = db.Column(db.Integer, 
                        primary_key=True)
    nama_role = db.Column(db.String(30), 
                          nullable=False)
    deskripsi = db.Column(db.String(256), 
                          nullable=True)
    
    def __repr__(self):
        return '<Role {}>'.format(self.name) 

class Akun(db.Model):

    __tablename__ = 'akun'
    
    username = db.Column(db.String(256), 
                         primary_key=True)
    password = db.Column(db.String(256), 
                         nullable=False)
    id_role = db.Column(db.Integer,
                        db.ForeignKey('role.id_role'),
                        nullable=False)
    role = db.relationship('Role', backref=db.backref('akun', lazy=True))
    
    
    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'password':
                value = hash_pass(value) 

            setattr(self, property, value)

    def __repr__(self):
         return '<Akun {}>'.format(self.username)


@login_manager.user_loader
def user_loader(username):
    return Akun.query.filter_by(username=username).first()


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = Akun.query.filter_by(username=username).first()
    return user if user else None