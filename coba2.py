import pandas as pd
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore")

url = 'https://id.wikipedia.org/wiki/Daftar_kecamatan_dan_kelurahan_di_Indonesia'
r  = requests.get(url)
data = r.text
soup = BeautifulSoup(data,'lxml')

a = soup.findAll('table', {"class":"wikitable"})
a = a[1:]

b = soup.findAll('span', {"class":"mw-headline"})
b = [a.find('a').text for a in b if a.find('a')]

kodes = []
names = []
areas = []
people = []
kecamatan = []
kelurahan = []
desa = []
provinsi = []

for j in range(len(a)):
    loop1 = a[j].findAll('tr')
    loop1 = loop1[2:-1]
    for k in range(len(loop1)):
        try:
            datas = loop1[k].find('td').parent.find_all('td')
            for i, td in enumerate(datas):
                if j==0 and j==10:
                    if i%9==1:
                        kodes.append(td.text.strip())
                        provinsi.append(b[j])
                    elif i%9==2:
                        names.append(td.text.strip())
                    elif i%9==3:
                        areas.append(td.text.strip())
                    elif i%9==4:
                        people.append(td.text.strip())
                    elif i%9==6:
                        kecamatan.append(td.text.strip())
                    elif i%9==7:
                        kelurahan.append(td.text.strip())
                    elif i%9==8:
                        desa.append(td.text.strip())
                else:
                    if i%8==1:
                        kodes.append(td.text.strip())
                        provinsi.append(b[j])
                    elif i%8==2:
                        names.append(td.text.strip())
                    elif i%8==3:
                        areas.append(td.text.strip())
                    elif i%8==4:
                        people.append(td.text.strip())
                    elif i%8==5:
                        kecamatan.append(td.text.strip())
                    elif i%8==6:
                        kelurahan.append(td.text.strip())
                    elif i%8==7:
                        desa.append(td.text.strip())
        except AttributeError as e:
            pass

df = pd.DataFrame()
df['Kode Wilayah'] = kodes
df['Provinsi'] = provinsi
df['Nama Wilayah'] = names
df['Luas Wilayah'] = areas
df['Penduduk'] = people
df['Kecamatan'] = kecamatan
df['kelurahan'] = kelurahan
df['desa'] = desa

df['Kode Wilayah'] = [x.replace('.','') for x in df['Kode Wilayah']]

def get_data_ktp(nomorktp, dataframe=df):
    nomorktp = str(nomorktp)
    
    if len(nomorktp)!=16:
        print('masukkan nomor KTP yang sesuai', end='\n')
        
    else:
        try:
            hasil = dataframe.loc[dataframe['Kode Wilayah']==nomorktp[:4], ['Provinsi','Nama Wilayah']].values[0]
            prov = hasil[0]
            wil = hasil[1]
            
        except IndexError:
            prov = 'Input Salah'
            wil = 'Input Salah'
            
        tanggal = int(nomorktp[6:8])
        bulan = nomorktp[8:10]
        tahun = int(nomorktp[10:12])
        
        if tahun<=9:
            tahun = '200' + str(tahun)
        else:
            tahun = '19' + str(tahun)
        
        if (tanggal>31) & (tanggal<72):
            gender = 'Perempuan'
            tanggal = tanggal - 40
            tanggal_lahir = str(tanggal) + '-' + bulan + '-' + tahun
        elif tanggal>71:
            gender = 'Input Salah'
            tanggal_lahir = 'Input Salah'
        else:
            gender = 'Laki-Laki'
            tanggal_lahir = str(tanggal) + '-' + bulan + '-' + tahun

        print('Provinsi \t:', prov)
        print('Kabupaten/Kota \t:', wil)
        print('Jenis Kelamin \t:', gender)
        print('Tanggal Lahir \t:', tanggal_lahir, end='\n')

test_ids = ['3522251205950001', '3506116506010005', '9907139507950005', '990713950795000500', '3401107507950005' ]

for ix, test_id in enumerate(test_ids):
    print(str(test_id))
    get_data_ktp(test_id)
    print('')
