from flask import render_template, redirect, url_for, request, session , jsonify, Response
from flask_login import login_required
from jinja2 import TemplateNotFound
import json
import cv2
from ultralytics import YOLO

from app import db, response
from app.perkuliahan import blueprint
from app.perkuliahan.jadwalForms import TambahJadwalForm
from app.model.kelasModel import Kelas
from app.model.perkuliahanModel import Perkuliahan
from app.controller import mataKuliahController, perkuliahanController, perkuliahanLogController


############## halaman jadwal routes ##############
@blueprint.route('/jadwal', methods=['GET', 'POST'])
@login_required
def jadwal():
    try: 
        role = session.get('role')
        if role == 'mahasiswa':
            user = {'role': role, 'username': session.get('username'), 'nama': session.get('nama'), 'kelas': session.get('kelas')}
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
            user = {'role': role, 'username': session.get('username'), 'nama': session.get('nama'), 'kelas': session.get('kelas')}
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
def generate_frame():
    # while True:
    camera = cv2.VideoCapture(0)
    detector = YOLO('app/face_recognition/yolov8n-face.pt')
    while True:
        success,frame = camera.read()
        if success:
            results = detector(frame, stream=True, max_det=1)
            for r in results: 
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else: 
            break
    
@blueprint.route('/jadwal/linimasa/tandai-presensi')
@login_required
def tandai_presensi():
    try:
        return render_template('perkuliahan/tandaiPresensi.html', user = {'username': session.get('username')} ) 
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500
        
@blueprint.route('/jadwal/linimasa/tandai-presensi/camera')
@login_required
def open_camera():
    try: 
        return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(e)
        return render_template('page-500.html'), 500

        
# @blueprint.route('/jadwal/linimasa/tandai-presensi/close_camera')
# @login_required
# def close_camera():
#     try: 
#         if camera.isOpened():
#             camera.release()
#             cv2.destroyAllWindows()
#         # return redirect(url_for('perkuliahan_blueprint.linimasa'))
#         # return response.success('SUCCESS', "success")
#         return jsonify({'status': 'success', 'message': 'Camera closed'})
#     except Exception as e:
#         print(e)
#         return render_template('page-500.html'), 500
