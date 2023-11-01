# CNN_Model
Este es un repositorio para el proyecto final de big data

En este proyecto se utiliza python y kafka

La idea del proyecto es que el producer tome una imagen de alguna carpeta local, la envie a un topic de kafka y el consumer revise el topic y si hay una imagen la muestre en la pagina de streamlit y de la prediccion del modelo

En el archivo modelo se crea un modelo de convolucion de varias capas que toma las imagenes de entrenamiento y es capaz de predecir las imagenes que reciba el consumer
