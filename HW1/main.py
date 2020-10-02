import numpy as np
import cv2, os
img = cv2.imread('lena.bmp')
row_size = img.shape[0]
col_size = img.shape[1]
if 'image' not in os.listdir():
    os.makedirs('image')

# Problem (a) upside-down lena.bmp
img_a = np.copy(img)
for row in range(row_size):
    for col in range(col_size):
        img_a[row,col] = img[-row,col]
cv2.imwrite('image/(a)lena.jpg', img_a)

# Problem (b) right-side-left lena.bmp
img_b = np.copy(img)
for row in range(row_size):
    for col in range(col_size):
        img_b[row,col] = img[row,-col]
cv2.imwrite('image/(b)lena.jpg', img_b)

# Problem (c) diagonally flip lena.bmp
img_c = np.copy(img)
for row in range(row_size):
    for col in range(col_size):
        img_c[row,col] = img[col, row]
cv2.imwrite('image/(c)lena.jpg', img_c)

# Problem (d) rotate lena.bmp 45 degrees clockwise
import imutils
img_d = np.copy(img)
img_d = imutils.rotate_bound(img_d, 45)
cv2.imwrite('image/(d)lena.jpg', img_d)

# Problem (e) shrink lena.bmp in half
img_e = np.copy(img)
img_e = imutils.resize(img, row//2, col//2)
cv2.imwrite('image/(e)lena.jpg', img_e)

# Problem (f) binarize lena.bmp at 128 to get a binary image
img_f = np.copy(img)
for row in range(row_size):
    for col in range(col_size):
        if img_f[row, col][0] >= 128:
            img_f[row, col] = [255, 255, 255]
        else:
            img_f[row, col] = [0, 0, 0]
cv2.imwrite('image/(f)lena.jpg', img_f)