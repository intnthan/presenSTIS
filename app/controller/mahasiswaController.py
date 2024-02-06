from app import response 

from app.model.mahasiswaModel import Mahasiswa
from app.model.kelasModel import Kelas

def index():
    try:
        # select all data from mahasiswa
        mahasiswa = Mahasiswa.query.all()
        data = formatArray(mahasiswa)
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
        'nim': data.nim,
        'nama': data.nama_mhs,
        'id_kelas': data.id_kelas,
        'embeddings': data.embeddings
    }
    
    return data

# show detail one data
def detail(nim):
    try:
        mahasiswa = Mahasiswa.query.filter_by(nim=nim).first()
        kelas = Kelas.query.filter(Kelas.id_kelas==mahasiswa.id_kelas).first()    
        
        if not mahasiswa:
            return response.badRequest([], 'Data mahasiswa tidak ditemukan')
        
        data= {
            'nim': mahasiswa.nim,
            'nama': mahasiswa.nama_mhs,
            'kelas': kelas.nama_kelas,
            'embeddings': mahasiswa.embeddings
        }
        
        return response.success(data, "success")
    
    except Exception as e:
        print(e)