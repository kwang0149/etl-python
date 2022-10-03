import pandas as pd
import os

# delete files if exist

if os.path.exists('pandas-ltmpt\\rankingxlsx.xlsx'):
    os.remove('pandas-ltmpt\\rankingxlsx.xlsx')


# extract file from url
def extract(source):
    return pd.read_html(source)[0]



# rename the header
def tidy(data):
    data.columns=['Ranking Nasional','Kenaikan Nasional',"NPSN",'Sekolah','Nilai Total','Provinsi','Kota/Kabupaten','Jenis']
    # remove "More.." in schools column
    for i, row in data.iterrows():
        x=data.at[i,'Sekolah']
        list_sekolah=x.split(' ')
        list_sekolah.pop(-1)
        dataset.at[i,'Sekolah']=' '.join(list_sekolah)

    # parse datatype in column 'Kenaikan Nasional' to int
    for i,row in data.iterrows():
        y=data.at[i,'Kenaikan Nasional']
        if isinstance(y,str) and y!='-':
            data.at[i,'Kenaikan Nasional']=int(y)
        else:
            data.at[i,'Kenaikan Nasional']=0



# create data based on city
def make_city_table(city):
    data=dataset[dataset["Kota/Kabupaten"]==city]
    data.insert(0,'Ranking Kota',range(1,1+len(data)))
    return data

# create data based on province
def make_province_table(province):
    data=dataset[dataset["Provinsi"]==province]
    data.insert(0,'Ranking Provinsi',range(1,1+len(data)))
    return data

# schools that have higher ranking than previous year
def rank_up():
    return dataset[dataset["Kenaikan Nasional"]>0]
    
# schools that have lower ranking or same ranking than previous year
def not_rank_up():
    return dataset[dataset["Kenaikan Nasional"]<=0]


# write all table to 1 excel file with multiple sheets
def load(path,city,province):
     writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
     dataset.to_excel(writer,index=False,sheet_name='top100')
     make_city_table(city).to_excel(writer,index=False,sheet_name='ranking_kota')
     make_province_table(province).to_excel(writer,index=False,sheet_name='ranking_provinsi')
     rank_up().to_excel(writer,index=False,sheet_name="sekolah_ranking_naik")
     not_rank_up().to_excel(writer,index=False,sheet_name="sekolah_ranking_tidak_naik")
     writer.save()
     writer.close()

# perform etl
# extract file from website
dataset=extract('https://top-1000-sekolah.ltmpt.ac.id/site/index')
# tidy up the data
tidy(dataset)
load('pandas-ltmpt\\rankingxlsx.xlsx','Kota Surabaya','Prov. Jawa Timur')
