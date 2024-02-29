from app import response

from app.model.kelasModel import Kelas
from app.model.mahasiswaModel import Mahasiswa

def index():
    try: 
        kelas = Kelas.query.all()
        data = formatArray(kelas)
        return response.success(data, "success")
    except Exception as e: 
        print(e)

def detail(id):
    try: 
        kelas = Kelas.query.filter_by(id_kelas=id).first()
        mahasiswa = Mahasiswa.query.filter(Mahasiswa.id_kelas==kelas.id_kelas)
        
        if not kelas:
            return response.badRequest([], 'Data kelas tidak ditemukan')
        
        dataMahasiswa = arrayMahasiswa(mahasiswa)
        data = singleDataKelas(kelas, dataMahasiswa)
        return response.success(data, "success")
        
    except Exception as e: 
        print(e)
        
        
def formatArray(datas):     
    array = []
    
    for i in datas: 
        array.append(singleObject(i))
        
    return array

def singleObject(data):
    data = {
        'id_kelas': data.id_kelas,
        'nama_kelas': data.nama_kelas,
        'tahun_ajaran': data.tahun_ajaran,
        'semester': data.semester
    }
    
    return data
    
def arrayMahasiswa(datas):
    array= []
    for i in datas:
        mahasiswa = {
            'nim': i.nim,
            'nama_mhs': i.nama_mhs,
            'embeddings': i.embeddings
        }
        array.append(mahasiswa)
    return array

def singleDataKelas(kelas, mahasiswa):
    data ={
        'id_kelas': kelas.id_kelas,
        'nama_kelas': kelas.nama_kelas,
        'tahun_ajaran': kelas.tahun_ajaran,
        'semester': kelas.semester,
        'mahasiswa': mahasiswa
    }
    
    return data