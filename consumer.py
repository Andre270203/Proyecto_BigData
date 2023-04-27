import streamlit as st
from kafka import KafkaConsumer
from PIL import Image
import numpy as np
import tensorflow as tf
import io
from tensorflow.keras.models import load_model

# Configurar consumidor de Kafka
consumer = KafkaConsumer('imagenes', bootstrap_servers=['localhost:9092'])

# Cargar el modelo entrenado
modelo = load_model('modelo_cargado.h5')

# Clases del modelo
idx_to_classes = {0: 'buildings', 1: 'forest', 2: 'glacier', 
                  3: 'mountain', 4: 'sea', 5: 'street'}

# Definir el estilo de la página
st.set_page_config(page_title="Página para recibir imágenes", page_icon=":camera:", layout="wide")

# Agregar un título principal y una descripción
st.title("Bienvenido a mi página de imágenes")
st.markdown("Carga una imagen y mira lo que sucede")

# Crear una columna para mostrar la imagen cargada
col1, col2 = st.columns([2, 3])

# Definir función para cargar la imagen
def cargar_imagen():
    for mensaje in consumer:
        with col1:
            st.header("Imagen cargada")
            # Obtener la imagen del mensaje
            imagen_bytes = mensaje.value
        
            # Convertir la imagen a formato PIL
            imagen_pil = Image.open(io.BytesIO(imagen_bytes))

            # Preprocesar la imagen para hacer la predicción
            imagen_pil = imagen_pil.resize((150, 150))
            imagen_array = np.array(imagen_pil)
            imagen_array = imagen_array / 255.0
            imagen_array = imagen_array[np.newaxis, :]
        
            # Hacer la predicción con el modelo
            prob = modelo.predict(imagen_array)
            pred = np.argmax(prob)
            clase_predicha = idx_to_classes[pred]
        
            # Mostrar la imagen en Streamlit
            st.image(imagen_pil, width=400)
            st.write('La imagen es de la clase:', clase_predicha)

# Ejecutar la función para cargar la imagen
cargar_imagen()