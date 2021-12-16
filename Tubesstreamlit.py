import pandas as pd
import json
import streamlit as st
import plotly.express as px
from PIL import Image


#Membuka file json
with open ("kode_negara_lengkap.json") as file :
    data = json.load (file)
#Menjadikan file json sebagai dataframe
df_json = pd.DataFrame(data)
#Membuka file csv
df = pd.read_csv('produksi_minyak_mentah.csv')

# Memilih column name,region,sub-region,alpha-3 pada file json
df_jsonsort = df_json[['name', 'region', 'sub-region','country-code','alpha-3']]

# Mengganti nama column alpha-3 menjadi kode_negara
df_jsonrename = df_jsonsort.rename(columns = {'alpha-3':'kode_negara'})

# Merge data csv dan json
df1 = pd.merge(df,df_jsonrename,on = 'kode_negara')
df1 = df1.rename(columns = {'name':'negara'})

#Membuat list negara dan tahun
list_negara = []
list_tahun = []
#Menambahkan negara menjadi kumulatif
for i in list(df1['negara']) :
    if i not in list_negara :
        list_negara.append(i)
#Menambahkan tahun menjadi kumulatif
for i in list(df1['tahun']) :
    if i not in list_tahun :
        list_tahun.append(i)

##########Sidebar###########

image = Image.open('logoitb.png')
st.sidebar.image(image, width=255,use_column_width ='always')
st.sidebar.markdown("<h1 style='text-align: center; color: #5C5B5B'>Institut Teknologi Bandung</h1>", unsafe_allow_html=True)

#Memunculkan pilihan daftar negara
daftarnegara = st.sidebar.selectbox("Daftar Negara",list_negara)
#Memunculkan pilihan daftar tahun
daftartahun = st.sidebar.selectbox("Daftar Tahun",list_tahun, key="daftartahun")
daftartahun = int(daftartahun)

##########Sidebar###########

#####Header#####

st.markdown("<h1 style='text-align: center; color: #5C5B5B'>Informasi Seputar Data Produksi Minyak Mentah dari Berbagai Negara di Dunia</h1>", unsafe_allow_html=True)

page_names = ['Grafik','Informasi dan Tabel']
page = st.radio('Which One ?',page_names)

#####Header#####

if page == 'Grafik' :
    ##########Nomer 1A##########
    st.subheader("Grafik Jumlah Produksi Minyak terhadap Waktu dari Suatu Negara")
    namanegara = df1[df1['negara'] == daftarnegara]
    namanegara1 = namanegara.to_dict()

#Plot Data
    fig = px.line(namanegara1, x = 'tahun', y = 'produksi',width = 700, height = 350)
    fig.update_layout(margin = dict(l=20, r=20, t=20, b=20), paper_bgcolor = "LightSteelBlue")
    st.write(fig)

##########Nomer 1B##########
    st.subheader(" Grafik Jumlah Produksi Minyak Terbesar pada Suatu Tahun")
    st.caption("**DAPAT MEMILIH TAHUN**")
    banyak = st.slider("Pilih banyaknya negara: ", min_value  = 1, max_value = 50)
    banyak = int(banyak)

    df2 = df1.loc[df1['tahun'] == daftartahun]
# Mengurutkan dari jumlah produksi terbesar
    df2 = df2.sort_values(by = ['produksi'], ascending = False)
    df3 = df2[:banyak]
    df4 = df3.to_dict()
#plot data
    fig1 = px.bar(df4, x = 'negara', y = 'produksi',width = 700, height = 350)
    fig1.update_layout(margin = dict(l=20, r=20, t=20, b=20), paper_bgcolor = "LightSteelBlue")
    fig1.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
    st.write(fig1)
   
##########Nomer 1C###########
    st.subheader(" Grafik dengan Jumlah Produksi Minyak Terbesar pada Keseluruhan Tahun")
    banyak2 = st.slider("Pilih banyaknya negara: ", min_value  = 1, max_value = 50, key="banyak2")
    banyak2 = int(banyak2)
# Membuat list untuk menampung data kumulatif
    list_kodenegara = []
    list_kumulatif = []
#Menambahkan kodenegara
    for i in list(df1['kode_negara']) :
        if i not in list_kodenegara :
            list_kodenegara.append(i)
#Menambahkan jumlah produksi kumulatif
    for i in list_negara :
        jml = df1.loc[df1['negara'] == i, 'produksi'].sum()
        list_kumulatif.append(jml)

# Membuat dataframe untuk data kumulatif
    dfkumulatif = pd.DataFrame(list(zip(list_negara,list_kodenegara,list_kumulatif)),
    columns = ['negara','kode negara','kumulatif'])

    dfkumulatif = dfkumulatif.sort_values(by = ['kumulatif'], ascending = False)
    dfkumulatif1 = dfkumulatif[:banyak2]
    dfkumulatif2 = dfkumulatif1.to_dict()

# Membuat plot data
    fig2 = px.bar(dfkumulatif2, x = 'negara', y = 'kumulatif',width = 700, height = 350)
    fig2.update_layout(margin = dict(l=20, r=20, t=20, b=20), paper_bgcolor = "LightSteelBlue")
    fig2.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5, opacity=0.6)
    st.write(fig2)

else :
    left_col, right_col = st.columns((1,1))

    df2 = df1.loc[df1['tahun'] == daftartahun]
# Mengurutkan dari jumlah produksi terbesar
    df2 = df2.sort_values(by = ['produksi'], ascending = False)

# Membuat list untuk menampung data kumulatif
    list_kodenegara = []
    list_kumulatif = []
#Menambahkan kodenegara
    for i in list(df1['kode_negara']) :
        if i not in list_kodenegara :
            list_kodenegara.append(i)
#Menambahkan jumlah produksi kumulatif
    for i in list_negara :
        jml = df1.loc[df1['negara'] == i, 'produksi'].sum()
        list_kumulatif.append(jml)
# Membuat dataframe untuk data kumulatif
    dfkumulatif = pd.DataFrame(list(zip(list_negara,list_kodenegara,list_kumulatif)),
    columns = ['negara','kode negara','kumulatif'])
    dfkumulatif = dfkumulatif.sort_values(by = ['kumulatif'], ascending = False)

# Nomer 1D Bagian 1
# Mencari data(kode,negara, region,subregion) untuk jumlah produksi terbesar
    jumlah_produksi = df2[:1].iloc[0]['produksi']
    kode_negara = df2[:1].iloc[0]['kode_negara']
    negara = df2[:1].iloc[0]['negara']
    region = df2[:1].iloc[0]['region']
    sub_region = df2[:1].iloc[0]['sub-region']

    left_col.markdown("**Jumlah produksi terbesar pada suatu tahun **",)
    left_col.caption("Tahun mengikuti pilihan")
    left_col.metric(label = "Nilai", value = jumlah_produksi)
    left_col.text("{} \n{} \n{} \n{}".format(negara, kode_negara,region,sub_region))

#Mencari data(kode,negara,region,subregion) untuk jumlah produksi terbesar kumulatif
    produksi_kumulatif = dfkumulatif[:1].iloc[0]['kumulatif']
    negara = dfkumulatif[:1].iloc[0]['negara']
    kode_negara = ""
    region = ""
    sub_region = ""

    for i in range(len(df_json)) :
        if list(df_json['name'])[i] == negara :
            kode_negara = list(df_json['alpha-3'])[i]
            region = list(df_json['region'])[i]
            sub_region = list(df_json['sub-region'])[i]

    left_col.markdown("**Jumlah produksi terbesar pada keseluruhan tahun adalah**",)
    left_col.metric(label = "Nilai", value = produksi_kumulatif)
    left_col.text("{} \n{} \n{} \n{}".format(negara, kode_negara,region,sub_region))
    

# Nomer 1D Bagian 2
# Membuat data frame untuk jumlah produksi terkecil (tidak sama dengan nol)
    dfterkecil =  df2[df2['produksi'] != 0]
    dfterkecil = dfterkecil.sort_values(by = ['produksi'], ascending = True)

    jumlah_produksi = dfterkecil[:1].iloc[0]['produksi']
    kode_negara = dfterkecil[:1].iloc[0]['kode_negara']
    negara = dfterkecil[:1].iloc[0]['negara']
    region = dfterkecil[:1].iloc[0]['region']
    sub_region = dfterkecil[:1].iloc[0]['sub-region']

    right_col.markdown("**Jumlah produksi terkecil pada suatu tahun adalah**")
    right_col.caption("Tahun mengikuti pilihan")
    right_col.metric(label = "Nilai", value = jumlah_produksi)
    right_col.text("{} \n{} \n{} \n{}".format(negara, kode_negara,region,sub_region))
    

# Membuat data frame untuk jumlah produksi terkecil (tidak sama dengan nol) kumulatif
    dfmin = dfkumulatif[dfkumulatif['kumulatif'] != 0]
    dfmin = dfmin.sort_values(by = ['kumulatif'], ascending = True)

    produksi_kumulatif = dfmin[:1].iloc[0]['kumulatif']
    negara = dfmin[:1].iloc[0]['negara']
    kode_negara = ""
    region = ""
    sub_region = ""

    for i in range(len(df_json)) :
        if list(df_json['name'])[i] == negara :
            kode_negara = list(df_json['alpha-3'])[i]
            region = list(df_json['region'])[i]
            sub_region = list(df_json['sub-region'])[i]

    right_col.markdown("**Jumlah produksi terkecil pada keseluruhan tahun adalah**",)
    right_col.metric(label = "Nilai", value = produksi_kumulatif )
    right_col.text("{} \n{} \n{} \n{}".format(negara, kode_negara,region,sub_region))

#Nomor 1D Bagian 3
    dfnol = df2[df2['produksi'] == 0]
    dfnol1 = dfnol.reindex(columns= ['negara','kode_negara','country-code','region','sub-region','produksi','tahun'])
    dfnol2 = dfnol1.rename(columns = {'country-code':'kode negara angka'})
    dfnol2 = dfnol2.drop(['produksi','tahun'], axis=1)

    dfkumulatifnol = dfkumulatif[dfkumulatif['kumulatif'] == 0]
    kodekumulatif = []
    kodeangkakumulatif = []
    regionkumulatif = []
    subregionkumulatif = []

    for i in range(len(dfkumulatifnol)) :
        for j in range(len(df_json)) :
            if list(dfkumulatifnol['negara'])[i] == list(df_json['name'])[j] :
                kodekumulatif.append(list(df_json['alpha-3'])[j])
                kodeangkakumulatif.append(list(df_json['country-code'])[j])
                regionkumulatif.append(list(df_json['region'])[j])
                subregionkumulatif.append(list(df_json['sub-region'])[j])

    dfkumulatifnol['kode negara'] = kodekumulatif
    dfkumulatifnol['kode negara angka'] = kodeangkakumulatif
    dfkumulatifnol['region'] = regionkumulatif
    dfkumulatifnol['sub-region'] = subregionkumulatif

    dfkumulatifnol1 = dfkumulatifnol.reindex(columns= ['negara','kode negara','kode negara angka','region','sub-region','kumulatif'])
    dfkumulatifnol2 = dfkumulatifnol1.drop(['kumulatif'], axis=1)

    st.subheader("Daftar Negara dengan Jumlah Produksi Nol pada Suatu Tahun")
    st.caption("Tahun mengikuti pilihan")
    st.dataframe(dfnol2)

    st.subheader("Daftar Negara dengan Jumlah Produksi Nol pada Keseluruhan Tahun")
    st.dataframe(dfkumulatifnol2)
