import cv2, os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
if 'image' not in os.listdir():
    os.makedirs('image')
    
img = cv2.imread('lena.bmp')
rowSize = img.shape[0]
colSize = img.shape[1]

def getHist(filename, image, mode='show'):
    # configure agg for drawing
    if mode == 'save':
        matplotlib.use('TKAgg')
    elif mode == 'show':
        matplotlib.use('agg')
    else:
        raise 'illegal mode'

    hist = [0 for i in range(256)]
    for r in range(rowSize):
        for c in range(colSize):
            hist[image[r,c][0]] += 1 

    plt.bar(range(256), hist, 1)
    plt.xlabel('Intensity')
    plt.ylabel('Counts')
    
    if mode == 'save':
        plt.savefig(f'./image/{filename}')
        print(f'{filename} has been written in image/')
    else:
        plt.show()
    plt.close()

# Problem (a) original image and its histogram
cv2.imwrite('./image/(A)lena.jpg', img)
getHist( '(A)histogram.jpg', img, 'save')

# Problem (b) image with intensity divided by 3 and its histogram
img_b = np.copy(img)
for r in range(rowSize):
    for c in range(colSize):
        I = img[r,c][0]
        img_b[r,c] = [I//3, I//3, I//3]
cv2.imwrite('./image/(B)lena.jpg', img_b)
getHist('(B)histogram.jpg', img_b, 'save')


# Problem (c) image after applying histogram equalization to (b) and its histogram
img_c = np.copy(img)
n = [0 for i in range(256)]
for r in range(rowSize):
    for c in range(colSize):
        n[img_b[r,c][0]] += 1 # counting number of each intesity

for i in range(1, 256):
    n[i] += n[i-1] # accumulating number of pixels which intesity <= i

for i in range(256):
    n[i] *= 255
    n[i] //= (rowSize*colSize) # distribute to 256-range by the ratio 

for r in range(rowSize):
    for c in range(colSize):
        I = n[img_b[r,c][0]]
        img_c[r,c] = [I, I, I]

cv2.imwrite('./image/(C)lena.jpg', img_c)
getHist('(C)histogram.jpg', img_c, 'save')