from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import login_required
from jinja2 import TemplateNotFound
from datetime import datetime
import json

from app.controller import perkuliahanController


routes = Blueprint('routes', __name__)


############## beranda routes ############## 
@routes.route('/')
@routes.route('/index')
@login_required
def beranda():
    if session:
        role = session.get('role')
        if role == 'mahasiswa':
            user = {'role': role, 'username': session.get('username'), 'nim': session.get('nim'), 'nama': session.get('nama'), 'kelas': session.get('kelas')}
            perkuliahan = perkuliahan_today()
            return render_template('index.html', user=user, perkuliahan=perkuliahan)
        else :
            user = {'role': role, 'username': session.get('username')}
            return render_template('index.html', user=user)
   
    else: 
        return redirect(url_for('authentication_blueprint.login'))
    
    
############### Get perkuliahan hari ini ##################
def perkuliahan_today():
    kelas = session.get('kelas')
    perkuliahan = perkuliahanController.perkuliahanToday(kelas).data
    if perkuliahan is not None:
        perkuliahan = json.loads(perkuliahan).get('data')
        print(perkuliahan)
        return perkuliahan
    else:
        print('Data perkuliahan tidak ditemukan!')
        return None
    
############## template routes ##############
# @routes.route('/<template>')
# @login_required
# def route_template(template):
#     try:
#         if not template.endswith('.html') : 
#             template += '.html'
        
#         user= session.get('user')
#         return render_template(template, user=user)
    
#     except TemplateNotFound:
#         return render_template('page-404.html'), 404
    
#     except:  # noqa: E722
#         return render_template('page-500.html'), 500