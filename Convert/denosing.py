import cv2
from matplotlib import pyplot as plt

cap = cv2.VideoCapture(r"C:\Data set\Video\ill\ill_compilate1.mp4")
# out = cv2.VideoWriter(r'C:\Data set\Video\heal\heal256BINARY.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10,(256,216), False)
r=True
frames = []


n=0

while r:
    r,img = cap.read()

    if r:
        plt.imshow(img, cmap="gray")
        plt.show()
        img = cv2.resize(img, (128,128), interpolation=cv2.INTER_AREA)
        img=img[:-20,:]
        img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        img = cv2.GaussianBlur(img, (5, 5), 5,cv2.BORDER_DEFAULT)
        ret, thresh1 = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
        plt.imshow(thresh1, cmap="gray")
        n+=1
        print(n)
        plt.show()
        # out.write(thresh1)
    else:
        break
# out.release()