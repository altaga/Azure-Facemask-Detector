import os
import numpy as np
import tensorflow as tf
import random
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
import tensorflow.keras
from tensorflow.keras.layers import Dense, Conv2D, InputLayer, Flatten, MaxPool2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator,img_to_array,load_img
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
import distutils
if distutils.version.LooseVersion(tf.__version__) <= '2.0':
    raise Exception('This notebook is compatible with TensorFlow 1.14 or higher, for TensorFlow 1.13 or lower please use the previous version at https://github.com/tensorflow/tpu/blob/r1.13/tools/colab/fashion_mnist.ipynb')

print("The number of images with facemask labelled 'yes':",len(os.listdir('Facemask-Opt-Dataset/facemask-dataset/yes')))
print("The number of images without facemask labelled 'no':",len(os.listdir('Facemask-Opt-Dataset/facemask-dataset/no')))

import cv2
import os

data = []
labels = []

mylist = os.listdir("Facemask-Opt-Dataset/facemask-dataset") # Set Dataset Folder

for x in mylist:
    mylist2 = os.listdir("Facemask-Opt-Dataset/facemask-dataset/"+str(x))
    label = str(x)
    for y in mylist2:
        # extract the class label from the folder name

        # load the input image (64x64) and preprocess it
        image = load_img("Facemask-Opt-Dataset/facemask-dataset/"+str(x)+"/"+str(y),color_mode="grayscale", target_size=(64, 64))
        image = img_to_array(image)
        image = preprocess_input(image)

        # update the data and labels lists, respectively
        data.append(image)
        labels.append(label)

# convert the data and labels to NumPy arrays
data = np.array(data, dtype="float32")
labels = np.array(labels)

# perform one-hot encoding on the labels
lb = LabelBinarizer()
labels = lb.fit_transform(labels)
labels = to_categorical(labels)

# partition the data into training and testing splits using 80% of
# the data for training and the remaining 20% for testing

(x_train, x_test,y_train, y_test) = train_test_split(data, labels,
                                                        test_size=0.20, stratify=labels, random_state=42)

print('Training data: {}, {}'.format(x_train.shape, y_train.shape))
print('Test data: {}, {}'.format(x_test.shape, y_test.shape))

model = tf.keras.models.Sequential([
    InputLayer(input_shape=(64, 64, 1), name='input_data'),
    Conv2D(64, (3,3), activation='relu'),
    MaxPool2D(pool_size=(2,2)),
    Conv2D(128, (3,3), activation='relu'),
    MaxPool2D(pool_size=(2,2)),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(2, activation='softmax', name='output_logits')
])
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])

from tensorflow.keras.callbacks import EarlyStopping
es = EarlyStopping(monitor='val_loss', mode='auto', verbose=1)

history = model.fit(x_train,y_train,validation_data=(x_test, y_test),steps_per_epoch=1000,epochs=30, verbose=1 ,callbacks=[es])
loss, accuracy = model.evaluate(x_test,y_test)

print("Test loss: {}".format(loss))
print("Test accuracy: {}".format(accuracy))
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT] # Uncomment for optimization
tflite_quantized_model = converter.convert()
os.makedirs('outputs', exist_ok=True)
open("outputs/converted_model.tflite", "wb").write(tflite_quantized_model)
print("Train Complete")