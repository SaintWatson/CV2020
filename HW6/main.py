import cv2
import numpy as np
def h(b,c,d,e):
    if b != c:
        return 's'
    elif c != d or c != e:
        return 'q'
    else:
        return 'r'
def Yokoi(table):
    label_table = np.copy(table)
    for r in range(64):
        for c in range(64):
            if table[r,c] == 0:
                continue
            x0 = table[r,c]
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
                label_table[r,c] = 5
            else:
                label_table[r,c] = stat['q']
    return label_table

img = cv2.imread('lena.bmp')
rowSize = img.shape[0]
colSize = img.shape[1]

threshold = 128
blueGraph = np.ndarray((64,64), int)
for r in range(0,rowSize,8):
    for c in range(0,colSize,8):
        if img[r,c][0] < threshold:
            img[r,c] = [0,0,0]
            blueGraph[r//8,c//8] = 0
        else:
            img[r,c] = [255,255,255]
            blueGraph[r//8,c//8] = 1

        for r_off in range(8):
            for c_off in range(8):
                img[r+r_off, c+c_off] = img[r,c]

result = Yokoi(blueGraph)


for r in range(64):
    for c in range(64):
        if result[r,c] == 0:
            print(' ', end='')
        else:
            print(result[r,c], end='')
    print()