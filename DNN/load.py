import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split

cap_heal = cv2.VideoCapture(r"C:\Data set\Video\heal\heal256BINARY.mp4")
cap_ill = cv2.VideoCapture(r"C:\Data set\Video\ill\ill256BINARY.mp4")
s=25000
def lod():

    frames_heal = []
    frames_ill=[]
    n=0

    while n<=30000:
        r,img = cap_heal.read()
        if r:
            n += 1
            # img = cv2.resize(img, (128, 108), interpolation=cv2.INTER_AREA)

            frames_heal.append(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
            print(n)
        else:


            break
    n=0
    while n<=50000:
        r1, img1 = cap_ill.read()
        if r1:
            n += 1
            # img1 = cv2.resize(img1, (128, 108), interpolation=cv2.INTER_AREA)
            frames_ill.append(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY))
            print(n)
        else:
            break
    return frames_heal,frames_ill

def data_lung(frames=80000,testS=0.01):
    frames_heal, frames_ill=lod()
    frames_heal=np.array(frames_heal,dtype=np.uint8)
    heal_dignps=np.zeros(len(frames_heal)).astype(np.uint8)
    # print(len(frames_heal))
    frames_ill=np.array(frames_ill,dtype=np.uint8)
    ill_dignps=np.ones(len(frames_ill)).astype(np.uint8)
    # print(len(frames_ill))
    X=np.vstack((frames_heal,frames_ill))
    del frames_heal,frames_ill
    y=np.append(heal_dignps,ill_dignps)
    del heal_dignps,ill_dignps
    # print(X.shape)
    # print(y.shape)
    X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=testS,random_state=42)
    return X_train[:frames],X_test[:frames],y_train[:frames],y_test[:frames]
# for i in range(10):
#     plt.imshow(X_train[i], cmap="gray")
#     print(y_train[i])
#     plt.show()
# np.savez("data_set",heal=frames_heal,ill=frames_ill)
