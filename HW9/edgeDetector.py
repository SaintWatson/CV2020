import numpy as np
import cv2

COLOR_WHITE = [255,255,255]
COLOR_BLACK = [0,0,0]

def dumpImg(title, img):
    cv2.imshow(title, img)
    cv2.waitKey()
    cv2.destroyAllWindows()
def Roberts(img, threshold):
    rowSize, colSize = img.shape[0:2]
    img_in = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_REFLECT)
    img_out = np.copy(img)

    for r in range(rowSize):
        for c in range(colSize):
            r1 = int(img_in[r+2,c+2][0]) - int(img_in[r+1,c+1][0])
            r2 = int(img_in[r+2,c+1][0]) - int(img_in[r+1,c+2][0])
            GM = ((r1*r1) + (r2*r2)) ** 0.5
            if GM >= threshold:
                img_out[r,c] = COLOR_BLACK
            else:
                img_out[r,c] = COLOR_WHITE
    return img_out

GRED_PREWITT = 1
GRED_SOBEL = 2
GRED_FREIANDCHEN = 2**0.5

def Grediant(img, threshold, mode):
    rowSize, colSize = img.shape[0:2]
    img_in = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_REFLECT)
    img_out = np.copy(img)

    for r in range(rowSize):
        for c in range(colSize):

            m = [int(img_in[r+x,c+y][0]) for x in range(3) for y in range(3)]
            r1 = m[6] + mode * m[7] + m[8] - m[0] - mode * m[1] - m[2]
            r2 = m[2] + mode * m[5] + m[8] - m[0] - mode * m[3] - m[6]
            GM = ((r1*r1) + (r2*r2)) ** 0.5

            if GM >= threshold:
                img_out[r,c] = COLOR_BLACK
            else:
                img_out[r,c] = COLOR_WHITE
    return img_out

COMP_KIRSCH = 0
COMP_ROBINSON = 1
def Compass(img, threshold, mode):
    rowSize, colSize = img.shape[0:2]
    img_in = cv2.copyMakeBorder(img, 1, 1, 1, 1, cv2.BORDER_REFLECT)
    img_out = np.copy(img)

    if mode == COMP_KIRSCH:
        kernel = [ [-3,-3,5,-3,0,5,-3,-3,5],
                    [-3,5,5,-3,0,5,-3,-3,-3],
                    [5,5,5,-3,0,-3,-3,-3,-3],
                    [5,5,-3,5,0,-3,-3,-3,-3],
                    [5,-3,-3,5,0,-3,5,-3,-3],
                    [-3,-3,-3,5,0,-3,5,5,-3],
                    [-3,-3,-3,-3,0,-3,5,5,5],
                    [-3,-3,-3,-3,0,5,-3,5,5] ]
    elif mode == COMP_ROBINSON:
        kernel = [ [-1,0,1,-2,0,2,-1,0,1],
                    [0,1,2,-1,0,1,-2,-1,0],
                    [1,2,1,0,0,0,-1,-2,-1],
                    [2,1,0,1,0,-1,0,-1,-2],
                    [1,0,-1,2,0,-2,1,0,-1],
                    [0,-1,-2,1,0,-1,2,1,0],
                    [-1,-2,-1,0,0,0,1,2,1],
                    [-2,-1,0,-1,0,1,0,1,2] ]

    for r in range(rowSize):
        for c in range(colSize):

            m = [int(img_in[r+x,c+y][0]) for x in range(3) for y in range(3)]

            r_max = np.max([np.dot(m, kernel[i]) for i in range(8)])

            if r_max >= threshold:
                img_out[r,c] = COLOR_BLACK
            else:
                img_out[r,c] = COLOR_WHITE
    return img_out

def NevatiaBabu(img, threshold):
    rowSize, colSize = img.shape[0:2]
    img_in = cv2.copyMakeBorder(img, 2,2,2,2, cv2.BORDER_REFLECT)
    img_out = np.copy(img)

    kernel = [[100,100,100,100,100,100,100,100,100,100,0,0,0,0,0,-100,-100,-100,-100,-100,-100,-100,-100,-100,-100],
        [100,100,100,100,100,100,100,100,78,-32 ,100,92,0,-92,-100,32,-78,-100,-100,-100,-100,-100,-100,-100,-100],
        [100,100,100,32,-100,100,100,92,-78,-100,100,100,0,-100,-100,100,78,-92,-100,-100,100,-32,-100,-100,-100],
        [-100,-100,0,100,100,-100,-100,0,100,100,-100,-100,0,100,100,-100,-100,0,100,100,-100,-100,0,100,100],
        [-100,32,100,100,100,-100,-78,92,100,100,-100,-100,0,100,100,-100,-100,-92,78,100,-100,-100,-100,-32,100],
        [100,100,100,100,100,-32,78,100,100,100,-100,-92,0,92,100,-100,-100,-100,-78,32,-100,-100,-100,-100,-100]]
    
    for r in range(rowSize):
            for c in range(colSize):

                m = [int(img_in[r+x,c+y][0]) for x in range(-1,4) for y in range(-1,4)]

                r_max = np.max([np.dot(m, kernel[i]) for i in range(6)])

                if r_max >= threshold:
                    img_out[r,c] = COLOR_BLACK
                else:
                    img_out[r,c] = COLOR_WHITE
    return img_out

    return 0