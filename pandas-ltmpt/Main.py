import pandas as pd
import os

# delete files if exist
if os.path.exists('ranking-utbk.xlsx'):
    os.remove('ranking-utbk.xlsx')
# read table from ltmpt website as a list
ranking_ltmpt=pd.read_html('https://top-1000-sekolah.ltmpt.ac.id/site/index')
# catch the first element (dataframe type)
data_ranking=ranking_ltmpt[0]
# rename the header
data_ranking.columns=['Ranking Nasional','Kenaikan Nasional',"NPSN",'Sekolah','Nilai Total','Provinsi','Kota/Kabupaten','Jenis']

# remove "More.." in schools column
for i, row in data_ranking.iterrows():
    x=data_ranking.at[i,'Sekolah']
    list_sekolah=x.split(' ')
    list_sekolah.pop(-1)
    data_ranking.at[i,'Sekolah']=' '.join(list_sekolah)

# parse datatype in column 'Kenaikan Nasional' to int
for i,row in data_ranking.iterrows():
    y=data_ranking.at[i,'Kenaikan Nasional']
    if isinstance(y,str) and y!='-':
        data_ranking.at[i,'Kenaikan Nasional']=int(y)
    else:
        data_ranking.at[i,'Kenaikan Nasional']=0

# schools in Surabaya City
ranking_sby=data_ranking[data_ranking["Kota/Kabupaten"]=="Kota Surabaya"]
ranking_sby.insert(0,'Ranking Kota',range(1,1+len(ranking_sby)))

# schools in Jawa Timur Province
ranking_jatim=data_ranking[data_ranking["Provinsi"]=="Prov. Jawa Timur"]
ranking_jatim.insert(0,'Ranking Provinsi',range(1,1+len(ranking_jatim)))

# schools that have higher ranking than previous year
sekolah_naik=data_ranking[data_ranking["Kenaikan Nasional"]>0]

# schools that have lower ranking or same ranking than previous year
sekolah_tidak_naik=data_ranking[data_ranking["Kenaikan Nasional"]<=0]

# write all table to 1 excel file with multiple sheets
path = 'pandas-ltmpt\\ranking-utbk.xlsx'
writer = pd.ExcelWriter(path, engine = 'xlsxwriter')
data_ranking.to_excel(writer,index=False,sheet_name='top100')
ranking_sby.to_excel(writer,index=False,sheet_name='ranking_sby')
ranking_jatim.to_excel(writer,index=False,sheet_name='ranking_jatim')
sekolah_naik.to_excel(writer,index=False,sheet_name="sekolah_ranking_naik")
sekolah_tidak_naik.to_excel(writer,index=False,sheet_name="sekolah_ranking_tidak_naik")
writer.save()
writer.close()
