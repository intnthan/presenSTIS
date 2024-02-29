from flask import render_template, redirect, url_for, request, session , jsonify, Response
from flask_login import login_required
from jinja2 import TemplateNotFound
import json

from geopy.distance import geodesic
import folium 

import cv2
from ultralytics import YOLO

from app import db, response
from app.perkuliahan import blueprint
from app.perkuliahan.jadwalForms import TambahJadwalForm
from app.model.kelasModel import Kelas
from app.model.perkuliahanModel import Perkuliahan
from app.model.mahasiswaModel import Mahasiswa
from app.controller import mataKuliahController, perkuliahanController, perkuliahanLogController
from app.face_recognition.face_recognition import faceRecognition


############## halaman jadwal routes ##############
@blueprint.route('/jadwal', methods=['GET', 'POST'])
@login_required
def jadwal():
    try: 
        role = session.get('role')
        if role == 'mahasiswa':
            user = {'role': role, 'nim': session.get('nim'), 'nama': session.get('nama'), 'kelas': session.get('kelas')}
        else :
            user = {'role': role, 'username': session.get('username')}
        
        # data jadwal kuliah 
        if user['role'] == 'mahasiswa':
            perkuliahan = json.loads(perkuliahanController.perkuliahanByKelas(user['kelas']).data).get('data')
        else:
            perkuliahan = json.loads(perkuliahanController.index().data).get('data')        
                
        # form tambah jadwal
        form = TambahJadwalForm()
        form.kelas.choices = [(kelas.id_kelas, kelas.nama_kelas) for kelas in Kelas.query.all()]
        form.mataKuliah.choices = [(mk['id_mk'], f"{mk['nama_mk']} - {mk['dosen']}") for mk in json.loads(mataKuliahController.indexWithDosen().data).get('data')]
        if form.validate_on_submit():
            perkuliahanController.add()
            return redirect(url_for('perkuliahan_blueprint.jadwal'))
        
        return render_template('jadwal.html', form=form, user=user, events=perkuliahan)

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except Exception as e:
        print(e)
        # return render_template('page-500.html'), 500
    
############## TextField pertemuan ##############
@blueprint.route('/jadwal/get_pertemuan/<kelas>/<mk>', methods=['GET'])
@login_required
def dropdown_pertemuan(kelas,mk):
    try: 
        # pertemuan = perkuliahanController.lastPertemuan(kelas, mk)
        pertemuan = json.loads(perkuliahanController.lastPertemuan(kelas, mk).data)
        
        if pertemuan:
            return pertemuan
        else:
           return jsonify({'status': 'error', 'message': 'Data dosen tidak ditemukan'})
       
    except Exception as e:
        print(e)
        
############## detail perkuliahan ##############
@blueprint.route('/jadwal/detail/<id>', methods=['GET', 'POST'])
@login_required
def detail_perkuliahan(id):
    try: 
        perkuliahan = Perkuliahan.query.filter_by(id_perkuliahan=id).first()
        form = TambahJadwalForm(formdata=request.form, obj=perkuliahan)

        if form.validate_on_submit():
            
            form.populate_obj(perkuliahan)

            # perkuliahanController.update(id)
            # db.session.add(perkuliahan)
            db.session.commit()
            return redirect(url_for('perkuliahan_blueprint.jadwal'))
        
            # print(perkuliahan)
            # return redirect(url_for('perkuliahan_blueprint.jadwal'))
        
    
    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except Exception as e:
        print(e)
        db.session.rollback()
        return render_template('page-500.html'), 500
    
############## linimasa perkuliahan ##############
@blueprint.route('/jadwal/linimasa', methods=['GET', 'POST'])
@login_required
def linimasa():
    try: 
        role = session.get('role')
        if role == 'mahasiswa':
            user = {'role': role, 'nim': session.get('nim'), 'nama': session.get('nama'), 'kelas': session.get('kelas')}
        else :
            user = {'role': role, 'username': session.get('username')}
        
        # data jadwal kuliah 
        if user['role'] == 'mahasiswa':
            perkuliahan = json.loads(perkuliahanController.perkuliahanByKelas(user['kelas']).data).get('data')
            # print(perkuliahan)
            for entry in perkuliahan: 
                # id_perkuliahan = entry['id_perkuliahan']
                id_perkuliahan = 6
            timelines = json.loads(perkuliahanLogController.perkuliahanLogByPerkuliahan(id_perkuliahan).data).get('data')

        else:
            perkuliahan = json.loads(perkuliahanController.index().data).get('data')        
        
        return render_template('perkuliahan/linimasa.html', user=user, events=perkuliahan, timelines=timelines)

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500

############## tandai presensi ##############
@blueprint.route('/jadwal/linimasa/tandai-presensi/pindai-wajah')
@login_required
def pindai_wajah():
    try: 
        nim = session.get('nim')
        embedding_path = Mahasiswa.query.filter_by(nim=nim).first().embeddings
        verification = faceRecognition()
        return Response(verification.face_detection(embedding_path, nim), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500

@blueprint.route('/jadwal/linimasa/tandai-presensi', methods=['GET','POST'])
@login_required
def tandai_presensi():    
    try:
        return render_template('perkuliahan/tandaiPresensi.html', user = {'username': session.get('username')})
               
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500
    
@blueprint.route('jadwal/linimasa/tandai-presensi/get-user-location', methods=['POST'])
@login_required
def get_user_location():
    stis_loc = {
        'latitude': -6.231439384294804,
        'longitude': 106.86661252383303
    }
    
    try:
        data = request.json
        if 'location' not in data:
            return jsonify({'status': 'error', 'message': 'Location not found'}), 400
        
        user_loc = data['location']
        if not user_loc:
            return jsonify({'status': 'error', 'message': 'Location data is empty'}), 400
        
        # distance = geodesic((stis_loc['latitude'], stis_loc['longitude']), (user_loc['latitude'], user_loc['longitude'])).meters
        distance = geodesic((stis_loc['latitude'], stis_loc['longitude']), (-6.22280112537061, 106.87912523723114)).meters
        mapObj = folium.Map(location=[stis_loc['latitude'], stis_loc['longitude']], zoom_start=18)
        folium.Circle([stis_loc['latitude'], stis_loc['longitude']], radius=50, color='blue', fill=True, fill_color='blue',  tooltip='Politeknik Statistika STIS').add_to(mapObj)
        # folium.Marker([user_loc['latitude'], user_loc['longitude']], tooltip='Anda di sini').add_to(mapObj)
        folium.Marker([-6.231684012474479, 106.86689936586203], tooltip='Anda di sini').add_to(mapObj)
        mapObj.get_root().render()      # render map objet
       
        data = {
            'distance': 20,
            'mapElements': mapObj.get_root()._repr_html_()      # render map object
        }
        
        return jsonify({'status': 'success', 'message': 'Location data received', 'data': data})
        
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500
        
@blueprint.route('jadwal/linimasa/tandai-presensi/ambil-presensi', methods=['GET', 'POST'])
@login_required
def ambilPresensi():
    try:
        data = request.json
        if 'id_perkuliahan' not in data or 'nim' not in data:
            return jsonify({'status': 'error', 'message': 'Data not found'}), 400
        
        id_perkuliahan = data['id_perkuliahan']
        nim = data['nim']
        perkuliahanLogController.add(id_perkuliahan, nim)
        return jsonify({'status': 'success', 'message': 'Presensi berhasil ditandai'})
        
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500



