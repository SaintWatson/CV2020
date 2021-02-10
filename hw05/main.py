import cv2, os
import numpy as np

if 'image' not in os.listdir():
    os.makedirs('image')

img = cv2.imread('lena.bmp')

def default_kernel(): # the octogonal 3-5-5-5-3 kernel
    k = []
    for i in range(-2,3):
        for j in range(-2,3):
            if abs(i*j) != 4 :
                k.append((i,j,0))
    return k

def dilation(img, kernel=default_kernel()): 
    rowSize = img.shape[0]
    colSize = img.shape[1]
    dimg = np.copy(img)

    for r in range(rowSize):
        for c in range(colSize):
            max_value = 0
            for node in kernel:
                rr = r + node[0] 
                cc = c + node[1] 
                if -1 < rr < rowSize and -1 < cc < colSize: 
                    if img[rr,cc][0] + node[2] > max_value:
                        max_value = img[rr,cc][0] + node[2]
            dimg[r,c] = [max_value, max_value, max_value]
    return dimg

def erosion(img, kernel=default_kernel()): 
    rowSize = img.shape[0]
    colSize = img.shape[1]
    eimg = np.copy(img)

    for r in range(rowSize):
        for c in range(colSize):
            min_value = 255
            for node in kernel:
                rr = r + node[0] 
                cc = c + node[1] 
                if -1 < rr < rowSize and -1 < cc < colSize:
                    if img[rr,cc][0] + node[2] < min_value:
                        min_value = img[rr,cc][0] + node[2]
            eimg[r,c] = [min_value, min_value, min_value]
    return eimg

dimg = dilation(img)
cv2.imwrite('./image/(A)dilation.jpg', dimg)
print('dilation is done')

eimg = erosion(img)
cv2.imwrite('./image/(B)erosion.jpg', eimg)
print('erosion is done')

oimg = dilation(eimg)
cv2.imwrite('./image/(C)opening.jpg', oimg)
print('opening is done')

cimg = erosion(dimg)
cv2.imwrite('./image/(D)closing.jpg', cimg)
print('closing is done')
