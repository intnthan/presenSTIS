from app import response, db
from flask import request
from datetime import datetime

from app.model.perkuliahanModel import Perkuliahan
from app.model.kelasModel import Kelas
from app.model.mataKuliahModel import MataKuliah



####################### READ FUNCTION ####################### 
def index():
    try: 
        perkuliahan = Perkuliahan.query.all()
        data = formatArray(perkuliahan)
        return response.success(data, "success")
    except Exception as e: 
        print(e)

def perkuliahanById(id_perkuliahan):
    try: 
        perkuliahan = Perkuliahan.query.filter_by(id_perkuliahan=id_perkuliahan).first()
        if not perkuliahan:
            return response.badRequest([], "Data perkuliahan tidak ditemukan!")
        data = singleObject(perkuliahan)
        return response.success(data, "success")
    except Exception as e: 
        print(e)
                
def lastPertemuan(id_kelas, id_mk):
    try: 
        lastPertemuan = Perkuliahan.query.filter_by(id_kelas=id_kelas, id_mk=id_mk).order_by(Perkuliahan.pertemuan.desc()).first()
        if not lastPertemuan:
            return response.success(1, "success")
        pertemuan = lastPertemuan.pertemuan + 1
        return response.success(pertemuan,"success")
    except Exception as e: 
        print(e)
        
def perkuliahanByKelas(id_kelas):
    try: 
        perkuliahan = Perkuliahan.query.filter_by(id_kelas=id_kelas).all()
        if not perkuliahan:
            return response.badRequest([], "Data perkuliahan tidak ditemukan!")
        data = formatArray(perkuliahan)
        return response.success(data, "success")
    except Exception as e: 
        print(e)

####################### CREATE FUNCTION #######################
def add():
    try: 
        id_kelas = request.form.get('kelas')
        id_mk = request.form.get('mataKuliah')
        pertemuan = request.form.get('pertemuan')
        jam_mulai = request.form.get('jam_mulai')
        jam_selesai = request.form.get('jam_selesai')
        tanggal = request.form.get('tanggal')
        ruangan = request.form.get('ruangan')
        
        db.session.add(Perkuliahan(id_kelas=id_kelas, 
                                id_mk=id_mk, 
                                pertemuan=pertemuan, 
                                jam_mulai=jam_mulai, 
                                jam_selesai=jam_selesai,
                                tanggal=tanggal, 
                                ruangan=ruangan))
        db.session.commit()
        
        return response.success('', 'Perkuliahan berhasil ditambahkan!')
    
    except Exception as e:
        print(e)

####################### UPDATE FUNCTION #######################
def update(id_perkuliahan):
    try: 
        jam_mulai = request.form.get('jam_mulai')
        jam_selesai = request.form.get('jam_selesai')
        tanggal = request.form.get('tanggal')
        ruangan = request.form.get('ruangan')
        
        perkuliahan = Perkuliahan.query.filter_by(id_perkuliahan=id_perkuliahan).first()
        perkuliahan.jam_mulai = jam_mulai
        perkuliahan.jam_selesai = jam_selesai
        perkuliahan.tanggal = tanggal
        perkuliahan.ruangan = ruangan
        
        db.session.commit()
        
        return response.success('', 'Perkuliahan berhasil diubah!')
    
    except Exception as e:
        print(e)
        
####################### DELETE FUNCTION #######################
def delete(id_perkuliahan):
    try: 
        perkuliahan = Perkuliahan.query.filter_by(id_perkuliahan=id_perkuliahan).first()
        if not perkuliahan: 
            return response.badRequest([], 'Data perkuliahan tidak ditemukan!')
        db.session.delete(perkuliahan)
        db.session.commit()
        
        return response.success('', 'Perkuliahan berhasil dihapus!')
    
    except Exception as e:
        print(e)


####################### FORMAT DATA #######################
def formatArray(datas):
    array = []
    for i in datas:
        array.append(singleObject(i))
    return array

def singleObject(data):
    data = {
        'id_perkuliahan' : data.id_perkuliahan,
        'id_kelas' : data.id_kelas,
        'kelas' : data.kelas.nama_kelas, 
        'id_mk' : data.id_mk,
        'kode_mk' : data.mata_kuliah.kode_mk,
        'matkul' : data.mata_kuliah.nama_mk,
        'pertemuan' : data.pertemuan,
        'jam_mulai' : data.jam_mulai.strftime('%H:%M'),
        'jam_selesai' : data.jam_selesai.strftime('%H:%M'),
        'tanggal' : format_date(data.tanggal),
        'start' : format_datetime(data.jam_mulai, data.tanggal),
        'end': format_datetime(data.jam_selesai, data.tanggal),
        'ruangan' : data.ruangan,
        'dosen' : data.mata_kuliah.dosen.nama_dosen
    }
    return data

def format_datetime(jam, tanggal):
    if jam is not None and tanggal is not None:
        return datetime.combine(tanggal, jam).strftime("%Y-%m-%d %H:%M:%S")
    return None

def format_date(date):
    if date is not None:
        return date.strftime('%Y-%m-%d')
    return None
