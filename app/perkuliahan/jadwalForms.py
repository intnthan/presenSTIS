from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, StringField, DateField, TimeField
from wtforms.validators import DataRequired

# form untuk tambah jadwal
class TambahJadwalForm(FlaskForm):
    
    # dropdown buat milih kelas
    kelas = SelectMultipleField('Kelas', 
                                id='inputKelas', 
                                validators=[DataRequired()])
    mataKuliah = SelectField('Mata Kuliah', 
                             id='inputMataKuliah', 
                             validators=[DataRequired()])
    pertemuan = StringField('Pertemuan',
                            id='inputPertemuan',
                            validators=[DataRequired()])
    tanggal = DateField('Tanggal',
                        validators=[DataRequired()])
    ruangan = StringField('Ruangan',
                          id='inputRuangan',
                          validators=[DataRequired()])
    jam_mulai = StringField('Jam Mulai',
                            validators=[DataRequired()])
    jam_selesai =StringField('Jam Selesai',
                             validators=[DataRequired()])