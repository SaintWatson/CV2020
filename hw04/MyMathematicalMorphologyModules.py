import cv2, os
import numpy as np

def default_kernel(): # the octogonal 3-5-5-5-3 kernel
    k = []
    for i in range(-2,3):
        for j in range(-2,3):
            if abs(i*j) != 4 :
                k.append((i,j))
    return k

def binarize(img, threshold): # input an image and output a 2D array
    rowSize = img.shape[0]
    colSize = img.shape[1]
    bimg = np.ndarray((rowSize, colSize), int)
    for r in range(rowSize):
        for c in range(colSize):
            intensity = img[r,c][0]
            if intensity >= threshold:
                bimg[r,c] = 1
            else:
                bimg[r,c] = 0
    return bimg

def bin2im(bimg): # input a 2D array and output a visible image
    rowSize = bimg.shape[0]
    colSize = bimg.shape[1]
    img = np.zeros((rowSize,colSize,3), np.uint8)
    for r in range(rowSize):
        for c in range(colSize):
            if bimg[r,c] == 1:
                img[r,c] = [255, 255, 255]
            else:
                img[r,c] = [0, 0, 0]
    return img

def dilation(bimg, kernel=default_kernel()): 
    rowSize = bimg.shape[0]
    colSize = bimg.shape[1]
    dimg = np.ndarray((rowSize, colSize), int)

    # for all the whites, whiten the pixel if (rr,cc) in the range of image
    for r in range(rowSize):
        for c in range(colSize):
            if bimg[r,c] == 1:
                for node in kernel:
                    rr = r + node[0] 
                    cc = c + node[1] 
                    if -1< rr <rowSize and -1< cc <colSize: 
                        dimg[rr,cc] = 1
    return dimg

def erosion(bimg, kernel=default_kernel()): 
    rowSize = bimg.shape[0]
    colSize = bimg.shape[1]
    eimg = np.ndarray((rowSize, colSize), int)

    # use a flag to detect the condition (1) (rr,cc) not in the range of image (2) (rr,cc) is black
    # once any condition is satified, the flag will be zero. Otherwise, the pixel will maintain white. 
    for r in range(rowSize):
        for c in range(colSize):
            flag = 1
            for node in kernel:
                rr = r + node[0] 
                cc = c + node[1] 
                if not (-1 < rr <rowSize) or not (-1< cc <colSize) or bimg[rr,cc] == 0:
                    flag = 0
                    continue
            eimg[r,c] = flag
    return eimg

def reverse(bimg):
    rowSize = bimg.shape[0]
    colSize = bimg.shape[1]
    rimg = np.ndarray((rowSize, colSize), int)

    for r in range(rowSize):
        for c in range(colSize):
            if bimg[r,c] == 0:
                rimg[r,c] = 1
            else:
                rimg[r,c] = 0
    return rimg

cornerA = [(0,-1), (0,0), (1,0)] # right-up corner which containing the origin
cornerB = [(-1,0), (0,1), (-1,1)] # right-up corner which not containing the origin

def hit_and_miss(bimg, kernel_J=cornerA, kernel_K=cornerB):
    rowSize = bimg.shape[0]
    colSize = bimg.shape[1]

    rimg = reverse(bimg)
    img1 = erosion(bimg, kernel_J)
    img2 = erosion(rimg, kernel_K)
    hamimg = np.ndarray((rowSize, colSize), int)

    # Do the intersection of img1 and img2
    for r in range(rowSize):
        for c in range(colSize):
            if img1[r,c] == img2[r,c]:
                hamimg[r,c] = img1[r,c]

    return hamimg