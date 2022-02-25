import pandas as pd
import streamlit as st
import plotly.express as px
import requests

st.set_page_config(page_title='EMPRESAS - MONTERIA',
                   page_icon=':bar_chart:',
                   layout="wide")
st.sidebar.image('empresa-icono2.png')
st.header("EMPRESAS REGISTRADAS EN MONTERIA CORDOBA")

# Sidebar
st.sidebar.markdown("# Selecciona el año, mes y día")
#----------------------DESDE AQUI EMPIEZAN LA PREDICCION-------------------------------
year = st.sidebar.slider(
    label="Año", min_value=2005, max_value=2025, value=2025
)
month = st.sidebar.slider(
    label="Mes", min_value=1, max_value=12, value=2
)
day = st.sidebar.slider(
    label="Dia", min_value=1, max_value=31, value=5
)

request_data = [
  {
    "year": year,
    "month": month,
    "day": day
  }
]
   
url_api='https://app-diplomado-python.herokuapp.com/predict'
data = str(request_data).replace("'", '"')
prediccion = requests.post(url=url_api, data=data).text

st.metric(
    value=f'{pd.read_json(prediccion)["cantidad_empresas"][0]}',
    label="cantidad de empresas registradas para la fecha seleccionada",
)

@st.cache
def cargar_datos(filename:str):
    return pd.read_csv(filename)

datos = cargar_datos('empresas.csv')
#st.write(datos)

st.markdown("Empresas Registradas por año")
st.plotly_chart(
    px.bar(
        datos.groupby(["YEAR-M"])
        .count()
        .reset_index(),
        color_discrete_sequence=px.colors.sequential.Aggrnyl,
        x="YEAR-M",
        y="conteo",
    ),
    
    use_container_width=True,
)

st.markdown(" Renovacion de Matriculas por año")
st.plotly_chart(
    px.bar(
        datos.groupby(["YEAR-R"])
        .count()
        .reset_index(),
        color_discrete_sequence=px.colors.sequential.Aggrnyl, #Aggrnyl,
        x="YEAR-R",
        y="conteo",
    ),
    
    use_container_width=True,
)
#----------------------Grafico de torta------------------------------
lista_nom = list(datos['MUNICIPIO'].unique())
opcion_nom = st.sidebar.selectbox(label="Selecione su municipio: ",
                          options=lista_nom)
mun = list(datos.columns)
mun.pop(mun.index('MUNICIPIO'))
mun.pop(mun.index('ULT-ANO_REN'))
mun.pop(mun.index('conteo'))
mun.pop(mun.index('YEAR-M'))
mun.pop(mun.index('MONTH-M'))
mun.pop(mun.index('DAY-M'))
mun.pop(mun.index('YEAR-R'))
mun.pop(mun.index('MONTH-R'))
mun.pop(mun.index('DAY-R'))
select_mun = st.selectbox('Seleciona la actividad comercial',
                          options=mun)

st.markdown("Registro de Empresas por municipio")
@st.cache
def pie_simple(df: pd.DataFrame, x: pd.DataFrame, y, Nom_municipio_filter: str):
    data = df.copy()
    data = data[data["MUNICIPIO"] == Nom_municipio_filter] 
    lista_top5=list(data.groupby('actividad_comercial').sum().reset_index().sort_values(by='conteo', ascending=False).head(5) ['actividad_comercial'])
    data['actividad_comercial']=data['actividad_comercial'].apply(lambda x: x if x in lista_top5 else 'Otro') 
    fig = px.pie(data, names=x, values=y, color_discrete_sequence=px.colors.sequential.Aggrnyl)
    
    return fig, data
pl, c = pie_simple(datos, select_mun, "conteo", opcion_nom)
st.plotly_chart(pl,use_container_width=True)

st.markdown("Registro de Empresas por mes")
@st.cache
def line_simple(df: pd.DataFrame, x: pd.DataFrame, y):
    data = df.copy()
    data = data[data["MONTH-M"] ==x]
    data=data.groupby(['MONTH-M','DAY-M','YEAR-M']).sum().reset_index().sort_values(by=['DAY-M','YEAR-M'])
    fig = px.area(data, x='DAY-M', y=y, color_discrete_sequence=px.colors.sequential.Aggrnyl, color='YEAR-M')
    return fig, data
pl, c = line_simple(datos, month, "conteo")
st.plotly_chart(pl,use_container_width=True)

#datos.groupby(["day"]).count().reset_index().sort_values(by="MUNICIPIO", ascending=False)

st.sidebar.markdown('---')
st.sidebar.write('Grupo 2 | Python para analisis de datos https://github.com/juditarrieta94')

