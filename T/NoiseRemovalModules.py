import numpy as np
import cv2
import random
from time import time
def dumpImg(title,img):
    cv2.imshow(title, img)
    cv2.waitKey()
    cv2.destroyAllWindows()
def Guassian_Noise(img, amplitude):
    rowSize = img.shape[0]
    colSize = img.shape[1]
    out = np.copy(img)
    for r in range(rowSize):
        for c in range(colSize):
            v = int(img[r,c][0] + amplitude * random.gauss(0,1))
            out[r,c] = [v,v,v]
    return out
def SNP_Noise(img, probability):
    rowSize = img.shape[0]
    colSize = img.shape[1]
    out = np.copy(img)
    for r in range(rowSize):
        for c in range(colSize):
            v = random.uniform(0,1)
            if v > 1-probability:
                v = 255
            elif v < probability:
                v = 0
            else:
                v = img[r,c][0]
            out[r,c] = [v,v,v]
    return out
def box_filter(img, size):
    rowSize, colSize = img.shape[0:2]
    m = size//2

    pimg = cv2.copyMakeBorder(img, m, m, m, m, cv2.BORDER_REFLECT)
    cimg = np.zeros((rowSize+2*m, colSize), np.uint8)
    oimg = np.copy(img)

    for r in range(rowSize + 2*m):
        for c in range(colSize):
            cimg[r,c] = sum([pimg[r,c+m+x][0] for x in range(-m,m+1)]) // size

    for r in range(rowSize):
        for c in range(colSize):
            V = sum([cimg[r+m+x,c] for x in range(-m,m+1)]) // size
            oimg[r,c] = [V,V,V]

    return oimg
def median_filter(img, size):
    rowSize, colSize = img.shape[0:2]
    m = size//2

    pimg = cv2.copyMakeBorder(img, m, m, m, m, cv2.BORDER_REFLECT)
    oimg = np.copy(img)

    M = []
    for x in range(-m,m+1):
        for y in range(-m,m+1):
            M.append((x,y))


    for r in range(rowSize):
        for c in range(colSize):
            L = [pimg[r+m+M[i][0],c+m+M[i][1]][0] for i in range(size*size)]
            med = np.median(L)
            oimg[r,c] = [med, med, med]

    return oimg
def SNR(img_signal, img_noise):
    rowSize, colSize = img_signal.shape[0:2]
    Is=[]
    In=[]
    for r in range(rowSize):
        for c in range(colSize):
            Is.append(img_signal[r,c][0])
            In.append(int(img_noise[r,c][0]) - int(img_signal[r,c][0]))

    varS = np.var(Is)
    varN = np.var(In)
    return 20 * np.log10((varS/varN)**0.5)