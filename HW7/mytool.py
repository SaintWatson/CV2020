import numpy as np
import cv2

def downSample(img):
    threshold = 128
    table = np.ndarray((64,64),int)
    rowSize = img.shape[0]
    colSize = img.shape[1]
    for r in range(0,rowSize,8):
        for c in range(0,colSize,8):
            if img[r,c][0] < threshold:
                img[r,c] = [0,0,0]
                table[r//8,c//8] = 0
            else:
                img[r,c] = [255,255,255]
                table[r//8,c//8] = 1

            for r_off in range(8):
                for c_off in range(8):
                    img[r+r_off, c+c_off] = img[r,c]
    return table
def h(b,c,d,e):
    if b != c:
        return 's'
    elif c != d or c != e:
        return 'q'
    else:
        return 'r'
def Yokoi(table,r,c):
    x0 = table[r,c]
    if x0==0:
        return 0
    x1 = table[r,c+1] if c!=63 else 0
    x2 = table[r-1,c] if r!=0 else 0
    x3 = table[r,c-1] if c!=0 else 0
    x4 = table[r+1,c] if r!=63 else 0
    x5 = table[r+1,c+1] if r!=63 and c!= 63 else 0
    x6 = table[r-1,c+1] if r!=0 and c!= 63 else 0
    x7 = table[r-1,c-1] if r!=0 and c!= 0 else 0
    x8 = table[r+1,c-1] if r!=63 and c!= 0 else 0
    k1 = h(x0,x1,x6,x2)
    k2 = h(x0,x2,x7,x3)
    k3 = h(x0,x3,x8,x4)
    k4 = h(x0,x4,x5,x1)


    stat = {'q':0, 'r':0, 's':0}
    for k in [k1,k2,k3,k4]:
        stat[k] += 1

    if stat['r'] == 4:
        return 5
    else:
        return stat['q']
def pairRelationship(table):
    rowSize = table.shape[0]
    colSize = table.shape[1]
    
    yk_img = np.zeros((rowSize, colSize),int)
    for r in range(rowSize):
        for c in range(colSize):
            yk_img[r,c] = Yokoi(table,r,c)


    pr_img = np.zeros((rowSize, colSize), bool)
    for r in range(rowSize):
        for c in range(colSize):
            x0 = yk_img[r,c]
            if x0 != 1:
                pr_img[r,c] = False
                continue

            x1 = yk_img[r,c+1] if (c+1) < colSize else 0
            x2 = yk_img[r-1,c] if (r-1) >= 0 else 0
            x3 = yk_img[r,c-1] if (c-1) >= 0 else 0
            x4 = yk_img[r+1,c] if (r+1) < rowSize else 0
            for x in [x1,x2,x3,x4]:
                if x == 1:
                    pr_img[r,c] = True
                    break
                else:
                    pr_img[r,c] = False
    return pr_img
def same(a,b):
    rowSize = a.shape[0]
    colSize = a.shape[1]
    for r in range(rowSize):
        for c in range(colSize):
            if a[r,c] != b[r,c]:
                return False
    return True
def myWrite(name,img):
    rowSize = img.shape[0] * 8
    colSize = img.shape[1] * 8
    out = np.ndarray((rowSize, colSize, 3), np.uint8)
    for r in range(0,rowSize,8):
        for c in range(0,colSize,8):
            if img[r//8,c//8] == 0:
                pixel = [0,0,0]
            else:
               pixel = [255,255,255]
            for roff in range(8):
                for coff in range(8):
                    out[r+roff, c+coff] = pixel
    cv2.imwrite(name,out)