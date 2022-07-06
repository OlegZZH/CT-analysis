import glob
import os
import shutil
import sys

import cv2
import numpy as np
import pydicom
from unrar import rarfile

np.set_printoptions(threshold=sys.maxsize)
width = 512
hieght = 512
channel = 1
fps = 10

needed_filter=["LUNG","Lung 1.5","Mediastinum","-Lung","HELICAL"]
for i in glob.glob(pathname=r"C:\Data set\22\Subject (469).rar", recursive=False,):
        files = []
        fileName_absolute = os.path.splitext(os.path.basename(i))[0]
        print(fileName_absolute)

        with rarfile.RarFile(i) as rar:
            rar.extractall(path=r"C:\Data set\temp")

        # for fname in glob.glob(pathname=r"C:\Data set\Video\{0}\**\*.dcm".format(fileName_absolute), recursive=False,):
        #     print("loading: {}".format(fname))
        #     files.append(pydicom.dcmread(fname))

        for root, dirs, file in os.walk(r"C:\Data set\22\Subject (469)"):
            for f in file:

                # print(os.path.join(root, f))
                files.append(pydicom.dcmread(os.path.join(root, f)))

        slices = []
        for f in files:
            if  hasattr(f, 'SliceLocation')and  f.SeriesDescription in needed_filter   :

                slices.append(f)

            else:
                if f.SeriesDescription in needed_filter:
                    print(f)


        slices = sorted(slices, key=lambda s: s.SliceLocation)
        slices= slices[::2]

        print(len(slices))
        image_2d_scaled=[]
        for s in slices:
            img=(s.pixel_array.astype(float))
            image_2d_scaled.append((np.maximum(img, 0) / img.max()) * 255.0)

        image_2d_scaled = np.uint8(image_2d_scaled)

        print(image_2d_scaled.shape)
        out = cv2.VideoWriter(r'C:\Data set\Video\{0}.mp4'.format(fileName_absolute), cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, hieght), False)
        for i in image_2d_scaled[1:]:
            out.write(i)
        out.release()
        shutil.rmtree(r"C:\Data set\temp")

# for i in image_2d_scaled[3:5]:
#     plt.imshow(i, cmap=plt.cm.gray)
#     plt.show()


