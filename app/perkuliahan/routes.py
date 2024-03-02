from flask import render_template, redirect, url_for, request, session , jsonify, Response, stream_with_context
from flask_login import login_required
from jinja2 import TemplateNotFound
import json

from geopy.distance import geodesic
import folium 

import time
import cv2
import numpy as np
import pickle
from ultralytics import YOLO
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from sklearn.metrics.pairwise import cosine_similarity

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
global marked 
global camera
camera = cv2.VideoCapture(0)
marked = False
 
def preprocess_image(face):
    image = cv2.resize(face, (224,224))
    image = np.expand_dims(face, axis=0)
    image = preprocess_input(image)
    return image 

def face_recognition(embedding_path, face):
    model = load_model('app/face_recognition/vgg16_model.h5')
    face = preprocess_image(face)
    
    # get embedding from database dan embedding from frame
    embedding = pickle.load(open(embedding_path, 'rb'))
    new_embedding = model.predict(face)[0,:]
    
    # verify face with cosine similarity
    similarity = cosine_similarity(embedding.reshape(1,-1), new_embedding.reshape(1,-1))[0][0]
    if(similarity > 0.8):
        return True, similarity
    else:
        return False, similarity     

def generate_camera(embedding_path, nim):
    detector = YOLO('app/face_recognition/yolov8n-face.pt')
    target_size = (224,224)
    global marked
   
    while camera.isOpened() : 
        success,frame = camera.read()
        if not success:
            break
        
        results = detector(frame, stream=True, max_det=1)
        for r in results: 
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                
                # mendapatkan wajah yang terdeteksi 
                face = frame[y1:y2, x1:x2]
                face = cv2.resize(face, target_size)
                matched = face_recognition(embedding_path, face)
                if (matched[0]): 
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, nim, (x1, y1-10),cv2.FONT_HERSHEY_SIMPLEX,  0.5, (0, 255, 0), 2)
                    marked = True
                    break
                
                else:
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255,255,255), 2)  
                    cv2.putText(frame, "Wajah tidak dikenali!", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX,  0.5,(0,0,255), 2)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        if marked:
            time.sleep(10)
            break
        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    camera.release()  

         
@blueprint.route('/jadwal/linimasa/tandai-presensi/pindai-wajah')
@login_required
def pindai_wajah():
    global marked
    
    nim = session.get('nim')
    embedding_path = Mahasiswa.query.filter_by(nim=nim).first().embeddings
    
    global camera
    camera = cv2.VideoCapture(0)
    try: 
        while not marked:
            return Response(generate_camera(embedding_path, nim), mimetype='multipart/x-mixed-replace; boundary=frame')
        
        camera.release()
        marked = False
        
    except Exception as e:
        print("error", e)
        
@blueprint.route('/jadwal/linimasa/tandai-presensi/pindai-wajah/marked')    
@login_required
def mark_attendance():
    nim = session.get('nim')
    global marked
    if not marked:
        return Response('data: failed\n\n', mimetype='text/event-stream' )  
    marked = False
    return Response('data: success\n\n', mimetype='text/event-stream' )  
    
@blueprint.route('/jadwal/linimasa/tandai-presensi/pindai-wajah/stop')
@login_required
def stop_pindai_wajah():
    camera.release()
    global marked
    marked = False
    return redirect(url_for('perkuliahan_blueprint.linimasa'))

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
        distance = geodesic((stis_loc['latitude'], stis_loc['longitude']), (-6.231684012474479, 106.86689936586203)).meters
        mapObj = folium.Map(location=[stis_loc['latitude'], stis_loc['longitude']], zoom_start=18)
        folium.Circle([stis_loc['latitude'], stis_loc['longitude']], radius=50, color='blue', fill=True, fill_color='blue',  tooltip='Politeknik Statistika STIS').add_to(mapObj)
        # folium.Marker([user_loc['latitude'], user_loc['longitude']], tooltip='Anda di sini').add_to(mapObj)
        folium.Marker([-6.231684012474479, 106.86689936586203], tooltip='Anda di sini').add_to(mapObj)
        mapObj.get_root().render()      # render map objet

        data = {
            'distance': distance,
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



