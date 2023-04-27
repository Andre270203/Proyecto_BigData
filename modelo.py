#importar las librerias necesarias
import matplotlib.pyplot as plt
import os
from PIL import Image

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import BatchNormalization, Conv2D, Dense, Dropout, Flatten, AvgPool2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator

#ruta de las carpetas que contienen las imagenes
train_path = '/home/andremf/BigData-project/seg_train'
test_path = '/home/andremf/BigData-project/seg_test/seg_test'

# Carga de las imagenes
img_gen = ImageDataGenerator(rescale=1./255,zoom_range=0.2,
                            width_shift_range=0.2,
                            height_shift_range=0.2, fill_mode='nearest')

train_loader = img_gen.flow_from_directory(
    directory = train_path, target_size = (150,150), 
    batch_size = 32, class_mode="categorical"
)
test_loader = img_gen.flow_from_directory(
    directory = test_path, target_size = (150,150), 
    batch_size = 32, class_mode="categorical"
)

idx_to_classes = {val:key for key, val in dict(train_loader.
                                            class_indices).items()}

# Construccion del modelo

modelo = Sequential()
# Convolution 1
modelo.add(Conv2D(32,kernel_size = (3,3), activation = "relu",
                  input_shape = (150,150,3)))
modelo.add(AvgPool2D(pool_size = (3,3)))
modelo.add(BatchNormalization())
modelo.add(Dropout(0.3))

# Convolution 2
modelo.add(Conv2D(64,kernel_size = (3,3), activation = "relu"))
modelo.add(AvgPool2D(pool_size = (3,3)))
modelo.add(BatchNormalization())
modelo.add(Dropout(0.3))

modelo.add(Flatten())
modelo.add(Dense(32, activation = "relu"))
modelo.add(Dense(6, activation = "softmax"))

modelo.compile(optimizer = "adam", loss = "categorical_crossentropy",
               metrics = ["accuracy"])

steps_train = len(train_loader)
steps_test = len(test_loader)

train_metric = modelo.fit(
    train_loader, steps_per_epoch = steps_train,
    epochs = 20, validation_data = test_loader,
    validation_steps = steps_test
)

train_metric.save("modelo_cargado.h5")
print("modelo guardado")

def display_accuracy() :
    # Summarize history for accuracy
    plt.plot(train_metric.history['accuracy'])
    plt.plot(train_metric.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig("Accuracy.png")

def display_loss() :
    # Summarize history for loss
    plt.plot(train_metric.history['loss'])
    plt.plot(train_metric.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig("Loss.png")

display_accuracy()
display_loss()