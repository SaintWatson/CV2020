import cv2, os
import numpy as np
import edgeDetector as ed

dname = 'image'
if dname not in os.listdir():
    os.mkdir(dname)

lena = cv2.imread('lena.bmp')

# (a) Laplacian1, threshold = 15
mask = ed.Laplacian(lena, 15, ed.LAP_TYPE1)
cv2.imwrite('./image/(a)L1.jpg', ed.zero_crossing(mask))

# (b) Laplacian2, threshold = 15
mask = ed.Laplacian(lena, 15, ed.LAP_TYPE2)
cv2.imwrite('./image/(b)L2.jpg', ed.zero_crossing(mask))

# (c) Minimum-variance Laplacian, threshold = 20
mask = ed.Laplacian(lena, 13, ed.LAP_MINVAR)
cv2.imwrite('./image/(c)MVL.jpg', ed.zero_crossing(mask))

# (d) Laplacian of Gaussian, threshold = 3000
mask = ed.Laplacian(lena, 3000, ed.LAP_GAUSS)
cv2.imwrite('./image/(d)LG.jpg', ed.zero_crossing(mask))

# (e) Difference of Gaussian, threshold = 1
mask = ed.Laplacian(lena, 1, ed.LAP_DIFFGAUSS)
cv2.imwrite('./image/(e)DG.jpg', ed.zero_crossing(mask))