from app import response, db
from flask import request

from app.model.perkuliahanLogModel import PerkuliahanLog


####################### READ FUNCTION #######################
def index():
    try: 
        # perkuliahanLog = PerkuliahanLog.query.order_by(PerkuliahanLog.id_perkuliahan_log.desc()).all()
        perkuliahanLog = PerkuliahanLog.query.all()
        data = formatArray(perkuliahanLog)
        return response.success(data, "success")
    except Exception as e: 
        print(e)
        
def perkuliahanLogByPerkuliahan(id_perkuliahan):
    try: 
        perkuliahanLog = PerkuliahanLog.query.filter_by(id_perkuliahan=id_perkuliahan).order_by(PerkuliahanLog.id_perkuliahan_log.desc()).all()
        if not perkuliahanLog:
            return response.badRequest([], "Data perkuliahan log tidak ditemukan!")
        data = formatArray(perkuliahanLog)
        return response.success(data, "success")
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
        'id_perkuliahan_log' : data.id_perkuliahan_log,
        'id_perkuliahan' : data.id_perkuliahan,
        'id_status_perkuliahan' : data.id_status_perkuliahan,
        'status_perkuliahan' : data.status_perkuliahan.status_perkuliahan,
        'jam' : data.jam.strftime('%H:%M:%S'),
    }

    return data