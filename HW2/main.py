import cv2, os
import numpy as np
if 'image' not in os.listdir():
    os.makedirs('image')
    
img = cv2.imread('lena.bmp')
rowSize = img.shape[0]
colSize = img.shape[1]

# Problem (a) a binary image (threshold at 128)
img_a = np.zeros((rowSize, colSize, 3), np.uint8)
for r in range(rowSize):
    for c in range(colSize):
        if img[r,c][0] >= 128:
            img_a[r,c] = [255, 255, 255]
        else:
            img_a[r,c] = [0, 0, 0]
cv2.imwrite('./image/(A)lena.jpg', img_a)
print('(A)lena.jpg has been written in image/')

# Problem (b) a histogram
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TKAgg') # configure agg for drawing

pixels = []
for r in range(rowSize):
    for c in range(colSize):
        pixels.append(img[r,c,0])
plt.hist(pixels, bins=[i for i in range(256)])
plt.xlabel('Intensity')
plt.ylabel('Counts')
plt.savefig('./image/(B)histogram.jpg')
print('(B)histogram.jpg has been written in image/')


# Problem (c) connected components(regions with + at centroid, bounding box)

# Step.1 Turn img_a into binary image
bmp = np.ndarray((rowSize, colSize), dtype=int)
for r in range(rowSize):
    for c in range(colSize):
        if img_a[r,c][0] == 255:
            bmp[r,c] = 1
        else:
            bmp[r,c] = 0 

# Step.2 Use flooding to connect the main component (over 500 pixels)

Q = [] # maintaining the flooding ready queue
over500 = [] # record the component which size is over 500 pixels
label = 2 # label from 2 because the original image have had label 0 and 1

def flooding(bmp, r, c, label):
    if bmp[r,c] != 1: # this pixel has been labeled, so we do nothing
        return label

    count = 0 # record the # of pixel in this component
    Q.append((r,c))

    while len(Q) != 0:
        p = Q.pop(0)
        count += 1
        r = p[0]
        c = p[1]
        bmp[r,c] = label

        # check : (1) if the neighbor in boundary (2) hasn't been label (3) not in the ready queue
        if r>0 and bmp[r-1,c] == 1 and (r-1,c) not in Q:
            Q.append((r-1,c))
        if c>0 and bmp[r,c-1] == 1 and (r,c-1) not in Q:
            Q.append((r,c-1))
        if r<rowSize-1 and bmp[r+1,c] == 1 and (r+1,c) not in Q:
            Q.append((r+1,c)) 
        if c<colSize-1 and bmp[r,c+1] == 1 and (r,c+1) not in Q:
            Q.append((r,c+1))

    if count >= 500:
        over500.append(label)

    return label+1

for r in range(rowSize):
    for c in range(colSize):
        label = flooding(bmp, r, c, label)

# Step.3 Update the boundary and output a demo btw
demo = np.copy(img_a)
boundary = [{'u':rowSize, 'b':0, 'l':colSize, 'r':0, 'r_': 0, 'c_':0, 'n':0} for i in  range(len(over500))] 
color = [(255,0,0),(0,255,0),(0,0,255),(0,255,255),(255,0,255)]

for r in range(rowSize):
    for c in range(colSize):
        if bmp[r,c] in over500:
            ID = over500.index(bmp[r,c])
            if r < boundary[ID]['u']:
                boundary[ID]['u'] = r
            if r > boundary[ID]['b']:
                boundary[ID]['b'] = r
            if c < boundary[ID]['l']:
                boundary[ID]['l'] = c
            if c > boundary[ID]['r']:
                boundary[ID]['r'] = c
            boundary[ID]['r_'] += r
            boundary[ID]['c_'] += c
            boundary[ID]['n'] += 1
            demo[r,c] = color[ID]
for cpn in boundary:
        cpn['r_'] //= cpn['n']
        cpn['c_'] //= cpn['n']
cv2.imwrite('./image/demo.jpg', demo)
print('demo.jpg has been written in image/')

# Step.4 Draw the rectangle
img_c = np.copy(img_a)
for i, cpn in enumerate(boundary):
        cv2.rectangle(img_c,(cpn['l'], cpn['u']), (cpn['r'], cpn['b']), color[i], 2)
        cv2.circle(img_c, (cpn['c_'], cpn['r_']), 1, color[i], 3)
cv2.imwrite('./image/(C)lena.jpg', img_c)
print('(C)lena.jpg has been written in image/')


