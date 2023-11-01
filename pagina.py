import streamlit as st
from PIL import Image

st.set_page_config(page_title="Proyecto BIGDATA", layout="wide")

# header
with st.container():
    st.title("Esto es una pagina para el proyecto final de big data")

uploaded_image = st.file_uploader("Carga una imagen", type=["jpg","jpeg","png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Imagen cargada")
else:
    st.write("Por favor carga una imagen")
