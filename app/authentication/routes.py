from flask import render_template, redirect, request, url_for, session
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from flask_bcrypt import Bcrypt

from app import login_manager
from app.authentication import blueprint
from app.authentication.forms import LoginForm, CreateAccountForm
from app.model.akunModel import Akun
from app.model.mahasiswaModel import Mahasiswa


bcrypt = Bcrypt()

@blueprint.route('/')
def route_default():
    return redirect(url_for('authentication_blueprint.login'))

# login
@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
      
        # read form data
        username = request.form['username']
        password = request.form['password']

        user = Akun.query.filter_by(username=username).first()
        
        if user: 
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                # store in session 
                session['role'] = user.role.nama_role
                session['username'] = user.username
                if session['role'] == 'mahasiswa':
                    nim = Mahasiswa.query.filter_by(username=username).first().nim
                    session['nim'] = nim
                    session['nama'] = Mahasiswa.query.filter_by(nim=nim).first().nama_mhs
                    session['kelas'] = Mahasiswa.query.filter_by(nim=nim).first().id_kelas
             
                return(redirect(url_for('authentication_blueprint.route_default')))
            
            # if user and password not match 
            return render_template('login.html',
                                   msg='Username atau password salah',
                                   form=login_form)
        else:
            return render_template('login.html',
                                   msg='Username tidak ditemukan',
                                   form=login_form)
    if not current_user.is_authenticated:
        return render_template('login.html',                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
                               form=login_form)
    
    return redirect(url_for('routes.beranda'))

# belum ada route buat register 

# route logout 
@blueprint.route('/logout')
def logout():
    logout_user()
    # delete session 
    session.pop('user', None)
    return redirect(url_for('authentication_blueprint.login'))

# kalo belum login, redirect to login page 
@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('authentication_blueprint.login'))


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('page-500.html'), 500