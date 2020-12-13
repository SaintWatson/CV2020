import numpy as np
import cv2

COLOR_WHITE = [255,255,255]
COLOR_BLACK = [0,0,0]

def dumpImg(title, img):
    cv2.imshow(title, img)
    cv2.waitKey()
    cv2.destroyAllWindows()

LAP_TYPE1 = 0
LAP_TYPE2 = 1
LAP_MINVAR = 2
LAP_GAUSS = 3
LAP_DIFFGAUSS = 4

def Laplacian(img, threshold, mode):

    rowSize, colSize = img.shape[0:2]
    if mode == LAP_TYPE1:
        kernel = [0,1,0,1,-4,1,0,1,0]
        h = 1
    elif mode == LAP_TYPE2:
        kernel = [1/3,1/3,1/3,1/3,-8/3,1/3,1/3,1/3,1/3]
        h = 1
    elif mode == LAP_MINVAR:
        kernel = [2/3, -1/3, 2/3, -1/3, -4/3, -1/3, 2/3, -1/3, 2/3]
        h = 1
    elif mode == LAP_GAUSS:
        kernel = [0,0,0,-1,-1,-2,-1,-1,0,0,0,0,0,-2,-4,-8,-9,-8,-4,-2,0,0,0,-2,-7,-15,-22,-23,-22,-15,-7,-2,0,-1,-4,-15,-24,-14,-1,-14,-24,-15,-4,-1,-1,-8,-22,-14,52,103,52,-14,-22,-8,-1,-2,-9,-23,-1,103,178,103,-1,-23,-9,-2,-1,-8,-22,-14,52,103,52,-14,-22,-8,-1,-1,-4,-15,-24,-14,-1,-14,-24,-15,-4,-1,0,-2,-7,-15,-22,-23,-22,-15,-7,-2,0,0,0,-2,-4,-8,-9,-8,-4,-2,0,0,0,0,0,-1,-1,-2,-1,-1,0,0,0]
        h = 5
    else:
        kernel = [-1,-3,-4,-6,-7,-8,-7,-6,-4,-3,-1,-3,-5,-8,-11,-13,-13,-13,-11,-8,-5,-3,-4,-8,-12,-16,-17,-17,-17,-16,-12,-8,-4,-6,-11,-16,-16,0,15,0,-16,-16,-11,-6,-7,-13,-17,0,85,160,85,0,17,-13,-7,-8,-13,-17,15,160,283,160,15,-17,-13,-8,-7,-13,-17,0,85,160,85,0,17,-13,-7,-6,-11,-16,-16,0,15,0,-16,-16,-11,-6,-4,-8,-12,-16,-17,-17,-17,-16,-12,-8,-4,-3,-5,-8,-11,-13,-13,-13,-11,-8,-5,-3,-1,-3,-4,-6,-7,-8,-7,-6,-4,-3,-1]
        h = 5
    
    padding = cv2.copyMakeBorder(img,h,h,h,h,cv2.BORDER_REFLECT)
    mask = np.zeros((rowSize, colSize), int)

    for r in range(rowSize):
        for c in range(colSize):
            m = [padding[r+x,c+y][0] for x in range(2*h+1) for y in range(2*h+1)]
            product = np.dot(m, kernel)
            if product >= threshold:
                mask[r,c] = 1
            elif product <= -1 * threshold:
                mask[r,c] = -1
            else:
                mask[r,c] = 0

    return mask

def zero_crossing(mask):
    padding = cv2.copyMakeBorder(mask,1,1,1,1,cv2.BORDER_REFLECT)
    rowSize, colSize = mask.shape[0:2]
    output = np.ndarray((rowSize, colSize, 3), np.uint8)

    for r in range(rowSize):
        for c in range(colSize):
            if padding[r+1,c+1] == 1:
                m = [padding[r+x,c+y] for x in range(3) for y in range(3)]
                for i in m:
                    if i==-1:
                        output[r,c] = COLOR_BLACK
                        break
                else:
                    output[r,c] = COLOR_WHITE
            else:
                output[r,c] = COLOR_WHITE
    return output
