import cv2, os
import numpy as np
import MyMathematicalMorphologyModules as m4

if 'image' not in os.listdir():
    os.makedirs('image')
    
img = cv2.imread('lena.bmp')
bimg = m4.binarize(img, 128)

dimg = m4.dilation(bimg)
output = m4.bin2im(dimg)
cv2.imwrite('./image/(A)dilation.jpg', output)
print('dilation is done')

eimg = m4.erosion(bimg)
output = m4.bin2im(eimg)
cv2.imwrite('./image/(B)erosion.jpg', output)
print('erosion is done')

oimg = m4.dilation(eimg)
output = m4.bin2im(oimg)
cv2.imwrite('./image/(C)opening.jpg', output)
print('opening is done')

cimg = m4.erosion(dimg)
output = m4.bin2im(cimg)
cv2.imwrite('./image/(D)closing.jpg', output)
print('closing is done')

hamimg = m4.hit_and_miss(bimg)
output = m4.bin2im(hamimg)
cv2.imwrite('./image/(E)hit-and-miss.jpg', output)
print('hit-and-miss is done')
