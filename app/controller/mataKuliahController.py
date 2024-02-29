from app import response 

from app.model.mataKuliahModel import MataKuliah
from app.model.dosenModel import Dosen

def index():
    try: 
        mata_kuliah = MataKuliah.query.all()
        data = formatArray(mata_kuliah)
        return response.success(data, "success")
    except Exception as e: 
        print(e)
        
def indexWithDosen():
    try: 
        mata_kuliah = MataKuliah.query.all()
        
        if not mata_kuliah:
            return response.badRequest([], 'Data mata kuliah tidak ditemukan')
        
        dosens = []
        for mk in mata_kuliah:
            dosen = Dosen.query.filter(Dosen.nip==mk.nip).first()
            dosens.append(dosen)
            
        dataDosen = arrayDosen(dosens)      
        data = formatArray(mata_kuliah, dataDosen)
    
        return response.success(data, "success")
    
    except Exception as e: 
        print(e)

def detail(id):
    try:
        mata_kuliah = MataKuliah.query.filter_by(id_mk=id).first()
        dosen = Dosen.query.filter(Dosen.nip==mata_kuliah.nip).first()
        
        if not mata_kuliah:
            return response.badRequest([], 'Data mata kuliah tidak ditemukan')
        
        dataDosen = arrayDosen(dosen)
        data = singleDataMataKuliah(mata_kuliah, dataDosen)
        
        return response.success(data, "success")
    
    except Exception as e:
        print(e)
        
def uniqueKodeMk():
    try:
        all_matkul = MataKuliah.query.all()
        unique_matkul = {MataKuliah.kode_mk: MataKuliah for MataKuliah in all_matkul}.values()
        # data = formatArray(all_matkul)
        # return response.success(data, "success")
        return unique_matkul
    except Exception as e:
        print(e)
        
def matkulByKodeMK(kode_mk):
    try:
        mata_kuliah = MataKuliah.query.filter_by(kode_mk=kode_mk).all()
        
        if not mata_kuliah:
            return response.badRequest([], 'Data mata kuliah tidak ditemukan')
        data = formatArray(mata_kuliah)
        return response.success(data, "success")
    
    except Exception as e:
        print(e)
        
def dosenMatkul(kode_mk):
    try: 
        mata_kuliah = MataKuliah.query.filter_by(kode_mk=kode_mk).all()
        
        if not mata_kuliah:
            return response.badRequest([], 'Data mata kuliah tidak ditemukan')
        
        dosens = []
        for mk in mata_kuliah:
            dosen = Dosen.query.filter(Dosen.nip==mk.nip).first()
            dosens.append(dosen)
        
        data = arrayDosen(dosens)
        return response.success(data, "success")
    except Exception as e:
        print(e)
        

def formatArray(datas, dosens=None):
    array = []
    
    if dosens is not None:
        for data, dosen in zip(datas, dosens):
            array.append(singleObject(data, dosen))
        
    else: 
        for i in datas: 
            array.append(singleObject(i))
        
    return array

def singleObject(data, dosen=None):
    if dosen is not None:
        data = {
            'id_mk': data.id_mk,
            'kode_mk': data.kode_mk,
            'nama_mk': data.nama_mk,
            'nip': data.nip,
            'jumlah_pertemuan': data.jumlah_pertemuan,
            'dosen': dosen["nama_dosen"]
        }
    else:
        data = {
            'id_mk': data.id_mk,
            'kode_mk': data.kode_mk,
            'nama_mk': data.nama_mk,
            'nip': data.nip,
            'jumlah_pertemuan': data.jumlah_pertemuan
        }
    
    return data

def arrayDosen(datas):
    array= []
    for i in datas:
        dosen = {
            'nip': i.nip,
            'nama_dosen': i.nama_dosen
        }
        array.append(dosen)
    return array

def singleDataMataKuliah(mata_kuliah, dosen):
    data ={
        'id_mk': mata_kuliah.id_mk,
        'kode_mk': mata_kuliah.kode_mk,
        'nama_mk': mata_kuliah.nama_mk,
        'nip': mata_kuliah.nip,
        'jumlah_pertemuan': mata_kuliah.jumlah_pertemuan,
        'dosen': dosen
    }
    return data