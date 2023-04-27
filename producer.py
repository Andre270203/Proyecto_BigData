import os
from kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092')

path = "/home/andremf/BigData-project/imagenes-test"

while True:
    files = os.listdir(path)
    if not files:
        print("La carpeta está vacía. Saliendo del programa.")
        break
    for file in files:
        if not file:
            print("La carpeta está vacía.")
        if file.endswith(".jpg") or file.endswith(".png"):
            file_path = os.path.join(path, file)
            with open(file_path, 'rb') as f:
                img_bytes = f.read()
            producer.send('imagenes', value=img_bytes, key=file.encode('utf-8'))
            os.remove(file_path)
            print(f"Imagen {file} enviada al topic 'imagenes'")
        else:
            print(f"El archivo {file} no es una imagen.")
    time.sleep(25)

#producer.close()