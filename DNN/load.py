# Модуль load.py
import cv2
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split


# Клас для завантаженя та поділу даних
class LoadFile:
    def __init__(self):

        self.cap_heal = cv2.VideoCapture(r"C:\Data set\Video\heal\healreversed.mp4")
        self.cap_ill = cv2.VideoCapture(r"C:\Data set\Video\ill\illreversed.mp4")
        self.s=25000

    def lod(self):
        """
        Завантаження даних
        :return:
        """
        frames_heal = []
        frames_ill=[]
        n=0

        while n<=1000:
            r,img = self.cap_heal.read()
            if r:
                n += 1
                img = cv2.resize(img, (128, 108), interpolation=cv2.INTER_AREA)

                frames_heal.append(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
                print(n)
            else:


                break
        n=0
        while n<=5000:
            r1, img1 = self.cap_ill.read()
            if r1:
                n += 1
                img1 = cv2.resize(img1, (128, 108), interpolation=cv2.INTER_AREA)
                frames_ill.append(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY))
                print(n)
            else:
                break
        return frames_heal,frames_ill

    def data_lung(self,frames=80000,testS=0.3):

        """
        Метод реалізує перемішування та поділ даних
        :param frames: Кількість знімків яку поверне метод
        :param testS: Розмір тестової вибірки в %
        :return: Дані для навчання та перевірки
        """
        frames_heal, frames_ill=self.lod()
        frames_heal=np.array(frames_heal,dtype=np.uint8)
        heal_dignps=np.zeros(len(frames_heal)).astype(np.uint8)
        frames_ill=np.array(frames_ill,dtype=np.uint8)
        ill_dignps=np.ones(len(frames_ill)).astype(np.uint8)
        X=np.vstack((frames_heal,frames_ill))
        del frames_heal,frames_ill
        y=np.append(heal_dignps,ill_dignps)
        del heal_dignps,ill_dignps

        X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=testS, shuffle=True)
        return X_train, X_test, y_train, y_test

