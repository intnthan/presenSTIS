from app import create_app, db, response
from flask import request, jsonify, abort

from app.model.akunModel import Akun

# menampilkan semua data akun
def index():
    try:
        # select all data from akun
        akun = Akun.query.all()
        data = formatArray(akun)
        return response.success(data, "success")
    except Exception as e:
        print(e)
        
# format array
def formatArray(datas):
    array = []
    
    for i in datas: 
        array.append(singleObject(i))
        
    return array
        
# format singleobject
def singleObject(data):
    data = {
        'username': data.username,
        'password': data.password,
        'id_role': data.id_role,
    }
    
    return data
    
    
