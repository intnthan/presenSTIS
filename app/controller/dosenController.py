from app import response 

from app.model.dosenModel import Dosen

def index():
    try: 
        dosen = Dosen.query.all()
        data = formatArray(dosen)
        return response.success(data, "success")
    except Exception as e: 
        print(e)
        
def detail(nip):
    try: 
        dosen = Dosen.query.filter_by(nip=nip).first()
        
        if not dosen:
            return response.badRequest([], 'Data dosen tidak ditemukan')
        
        data = singleObject(dosen)
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
        'nip': data.nip,
        'nama_dosen': data.nama_dosen
    }
    
    return data