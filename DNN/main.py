import os

from matplotlib import pyplot as plt

# os.environ["CUDA_VISIBLE_DEVICES"]="-1"
from load import LoadFile
import numpy as np
from tensorflow import keras
import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D


class NN:
    def __init__(self):
        ld=LoadFile()
        X_train, X_test, y_train, y_test = ld.data_lung()

        self.x_train = X_train / 255
        self.x_test = X_test / 255
        del X_train, X_test
        # print(y_train)
        self.y_train_cat = keras.utils.to_categorical(y_train, 2)
        self.y_test_cat = keras.utils.to_categorical(y_test, 2)
        del y_train, y_test
        self.x_train = np.expand_dims(self.x_train, axis=3)
        self.x_test = np.expand_dims(self.x_test, axis=3)

        print(self.y_train_cat)
        gpus = tf.config.experimental.list_physical_devices('GPU')
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        self._model = keras.Sequential([
            Conv2D(32, (3, 3), padding='same', activation='relu', input_shape=(108, 128, 1)),
            MaxPooling2D((2, 2), strides=2),
            Conv2D(64, (3, 3), padding='same', activation='relu'),
            MaxPooling2D((2, 2), strides=2),
            Flatten(),
            Dense(128, activation='relu'),
            Dense(2, activation='softmax')
        ])

        print(self._model.summary())  # вывод структуры НС в консоль

        self._model.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['binary_accuracy'])

    def learn(self):
        self.his = self._model.fit(self.x_train, self.y_train_cat, epochs=3, batch_size=1,
                        validation_data=(self.x_test, self.y_test_cat))  # , validation_data=(x_test,y_test_cat)

    def save(self):
        fig, ax = plt.subplots()
        ax.plot(self.his.history["loss"], label='loss')
        ax.plot(self.his.history["val_loss"], label='val_loss')
        ax.legend()
        plt.show()
        self._model.save("lung_model30000_50000")

    def use(self):
        p=self._model.predict(self.x_test)
        tr=self.y_test_cat
        accu=np.around (p)==np.around(tr)

        t=0
        f=0

        for i in accu:
            if i.all():
                t+=1
            else:
                f+=1

        print("True:{0} |   False:{1}".format(t,f))

if __name__ == '__main__':
    nn=NN()
    nn.learn()
    # nn.use()