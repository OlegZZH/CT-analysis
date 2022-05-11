import os
import numpy as np
from tensorflow import keras
os.environ["CUDA_VISIBLE_DEVICES"]="-1"
from load import data_lung

X_train, X_test, y_train, y_test=data_lung(frames=30000,testS=0.01)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

model_loaded=keras.models.load_model("lung_model15000_25000V2")
x_train = X_train / 255
y_train_cat = keras.utils.to_categorical(y_train, 2)
t = 0
f = 0
print(x_train[:1].shape)
p = model_loaded.predict(x_train)

for i,j in zip(p,y_train_cat):

    if (np.around (i)==np.around(j)).all():
        t+=1
    else:
        f+=1


print("True:{0} |   False:{1}".format(t,f))
