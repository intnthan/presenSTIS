from app import db
from flask import request
from app.model import blueprint 
from app.controller import akunController
from app.controller import mahasiswaController
from app.controller import kelasController
from app.controller import perkuliahanController
from app.controller import dosenController

@blueprint.route('/akun', methods=['GET'])
def akun():
    # return akunController.index()
    pass

@blueprint.route('/mahasiswa/<nim>', methods=['GET'])
def detailMahasiswa(nim):
    # return mahasiswaController.detail(nim)
    pass

@blueprint.route('/perkuliahan', methods=['GET', 'POST'])
def perkuliahan():
    # if request.method == 'GET':
    #     return perkuliahanController.index()
    # elif request.method == 'POST':
    #     return perkuliahanController.add()
    pass
    
@blueprint.route('/perkuliahan/<id_perkuliahan>', methods=['GET', 'PUT', 'DELETE']) 
def perkuliahanDetail(id_perkuliahan):
    # if request.method == 'GET':
    #     return perkuliahanController.detail(id_perkuliahan)
    # elif request.method == 'PUT':
    #     return perkuliahanController.update(id_perkuliahan)
    # elif request.method == 'DELETE':
    #     return perkuliahanController.delete(id_perkuliahan)
    pass