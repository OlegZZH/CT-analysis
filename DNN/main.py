import os
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
from load import data_lung
import numpy as np
from tensorflow import keras
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D

X_train, X_test, y_train, y_test=data_lung()

x_train = X_train / 255
x_test = X_test / 255
del X_train,X_test
# print(y_train)
y_train_cat = keras.utils.to_categorical(y_train, 2)
y_test_cat = keras.utils.to_categorical(y_test, 2)
del y_train,y_test
x_train = np.expand_dims(x_train, axis=3)
x_test = np.expand_dims(x_test, axis=3)


print(y_train_cat)
model = keras.Sequential([
    Conv2D(32, (3,3), padding='same', activation='relu', input_shape=(216, 256, 1)),
    MaxPooling2D((2, 2), strides=2),
    Conv2D(64, (3,3), padding='same', activation='relu'),
    MaxPooling2D((2, 2), strides=2),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(2,  activation='softmax')
])

print(model.summary())      # вывод структуры НС в консоль

model.compile(optimizer='adam',
             loss='binary_crossentropy',
             metrics=['binary_accuracy'])


his = model.fit(x_train, y_train_cat, epochs=3, validation_split=0.2)

p=model.predict(x_test)
tr=y_test_cat
accu=np.around (p)==np.around(tr)

t=0
f=0

for i in accu:
    if i.all():
        t+=1
    else:
        f+=1

print("True:{0} |   False:{1}".format(t,f))
model.save("lung_model15000_25000")