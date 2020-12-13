import cv2, os
import numpy as np
import edgeDetector as ed

dname = 'image'
lena = cv2.imread('lena.bmp')
if dname not in os.listdir():
    os.mkdir(dname)

# (a)Robert's Operator: 15
img_a = ed.Roberts(lena, 15)
cv2.imwrite('./image/(a)Robert.jpg', img_a)

# (b)Prewitt's Operator: 35
img_b = ed.Grediant(lena, 35, ed.GRED_PREWITT)
cv2.imwrite('./image/(b)Prewitt.jpg', img_b)

# (c)Sobel's Operator: 55
img_c = ed.Grediant(lena, 55, ed.GRED_SOBEL)
cv2.imwrite('./image/(c)Sobel.jpg', img_c)

# (d)Frei and Chen gradient Operator: 50
img_d = ed.Grediant(lena, 50, ed.GRED_FREIANDCHEN)
cv2.imwrite('./image/(d)FC.jpg', img_d)

# (e)Kirsch compass Operator: 135
img_e = ed.Compass(lena, 135, ed.COMP_KIRSCH)
cv2.imwrite('./image/(e)Kirsch.jpg', img_e)

# (f)Robinson compass operator: 45
img_f = ed.Compass(lena, 45, ed.COMP_ROBINSON)
cv2.imwrite('./image/(f)Robinson.jpg', img_f)

# (g)    operator: 12500
img_g = ed.NevatiaBabu(lena, 12500)
cv2.imwrite('./image/(g)NB.jpg', img_g)


