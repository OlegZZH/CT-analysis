import numpy as np
from tensorflow import keras

from load import data_lung

X_train, X_test, y_train, y_test=data_lung(frames=2500,testS=0.1)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

model_loaded=keras.models.load_model("lung_model24000")
x_train = X_train / 255
y_train_cat = keras.utils.to_categorical(y_train, 2)
t = 0
f = 0
print(x_train[:1].shape)


for i,j in zip(x_train,y_train_cat):
    # plt.imshow(i)
    # plt.show()
    # print(np.expand_dims(i,axis=0).shape)
    p = model_loaded.predict(np.expand_dims(i,axis=0))


    # print("predict:{0}  |   true:{1}".format(np.around (p),np.around(tr)))



    if (np.around (p)==np.around(j)).all():
        t+=1
        # print(True)
    else:
        # print(False)
        f+=1
        # plt.imshow(i,cmap="gray")
        # plt.show()
    # print("predict:{0}  |   true:{1}".format(np.around (p),np.around(tr)))

print("True:{0} |   False:{1}".format(t,f))
