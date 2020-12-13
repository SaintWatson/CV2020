import cv2
import numpy as np
import mytool

img = cv2.imread('lena.bmp')
rowSize = img.shape[0]
colSize = img.shape[1]

ori_img = mytool.downSample(img)
lst_img = np.copy(ori_img)
mytool.myWrite('./image/0.jpg', ori_img)

rd=1
while(True):
    marked_img = mytool.pairRelationship(ori_img)
  
    for r in range(rowSize//8):
        for c in range(colSize//8):
            if marked_img[r,c] and (mytool.Yokoi(ori_img,r,c) == 1):
                ori_img[r,c] = 0

    mytool.myWrite(f'./image/{rd}.jpg',ori_img)
    if(mytool.same(lst_img, ori_img)):
        break

    lst_img = np.copy(ori_img)
    rd += 1