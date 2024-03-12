from app import response, db
from flask import request
from datetime import datetime

from app.model.presensiModel import Presensi


####################### READ FUNCTION #######################
def index():    
    try: 
        presensi = Presensi.query.all()
        data = formatArray(presensi)
        return response.success(data, "success")
    except Exception as e: 
        print(e)
 
def presensiByNimIdPerkuliahan(nim, id_perkuliahan):
    try: 
        presensi = Presensi.query.filter_by(nim=nim, id_perkuliahan=id_perkuliahan).all()
        if not presensi:
            data = None
            return response.success(data, "Data presensi tidak ditemukan!")
        data = formatArray(presensi)
        return response.success(data, "success")
    except Exception as e: 
        print(e)

def isPresensi(nim, id_perkuliahan):
    try: 
        presensi = Presensi.query.filter_by(nim=nim, id_perkuliahan=id_perkuliahan).all()
        if not presensi:
            return False
        else : 
            data = formatArray(presensi)
            return response.success(data, "success")
    except Exception as e: 
        print(e)

####################### CREATE FUNCTION #######################
def add(nim, id_perkuliahan):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try: 
        db.session.add(Presensi(nim=nim, 
                                id_perkuliahan=id_perkuliahan, 
                                waktu = current_time,
                                id_status=1,))
        
        db.session.commit()
        
        return response.success([], "Presensi berhasil ditambahkan!")
    except Exception as e:
        print(e)
        return response.badRequest([], "Terdapat kesalahan dalam menambahkan presensi")
    
####################### FORMAT DATA #######################        
def formatArray(datas):
    array = []
    for i in datas:
        array.append(singleObject(i))
    return array

def singleObject(data):
    data = {
        'id_presensi' : data.id_presensi,
        'nim' : data.nim,
        'id_perkuliahan' : data.id_perkuliahan,
        'waktu' : data.waktu.strftime('%H:%M:%S'),
        'id_status' : data.id_status,
        'status': data.status_presensi.status
    }
    return data