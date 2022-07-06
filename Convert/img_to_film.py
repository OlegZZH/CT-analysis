import cv2
import numpy as np

f = [r"C:\Data set\Video\ill\ill_compilate1.mp4"]
# for root, dirs, files in os.walk(r"C:\Data set\Video\heal"):
# 	for file in files:
# 		if(file.endswith(".mp4")):
# 			f.append(os.path.join(root, file))
f = np.array(f)
# print(f)
arr = np.empty((0, 512, 512))
# out = cv2.VideoWriter(r'C:\Data set\Video\healthy\heal_compilate1.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10,(512, 512), False)

for i in f:
    print(i)
    n = 0
    cap = cv2.VideoCapture(i)
    ret = True
    frames = []
    while ret:
        ret, img = cap.read()  # read one frame from the 'capture' object; img is (H, W, C)
        if ret:
            n += 1
            frames.append(img)

    # video = np.array(frames)
    # video=video[:,:,:,0]
    # start =int(video.shape[0]*0.15)
    # end =int(video.shape[0]*0.6)

    # for i in video[start:end,:,:]:
    # 	n+=1
    # 	out.write(i)
    print(n)

# arr=np.vstack((arr,video[start:end,:,:]))
# out.release()
# arr=np.array(arr,dtype=np.uint8)
# print(arr[1])
# print(arr.shape)

# f = np.uint8(f)
# # print(f[0].shape)
# # plt.imshow(f[0], cmap=plt.cm.gray)
# # plt.show()
#
# for i in f:
# 	# print(n)
#
#
