import cv2, os
import numpy as np
import NoiseRemovalModules as nr

noiseImgNames = ["GS_L", "GS_H", "SNP_L", "SNP_H"]
dirname = './image/'
lena = cv2.imread('lena.bmp')

if 'image' not in os.listdir():
    os.mkdir('image')
    for i in range(4):
        os.mkdir(dirname + noiseImgNames[i])

    print('Creating Noise Image..')

    GS10 = nr.Guassian_Noise(lena, 10)
    cv2.imwrite( dirname + noiseImgNames[0] + './origin.jpg', GS10)

    GS30 = nr.Guassian_Noise(lena, 30)
    cv2.imwrite( dirname + noiseImgNames[1] + './origin.jpg', GS30)

    SNP005 = nr.SNP_Noise(lena, 0.05)
    cv2.imwrite( dirname + noiseImgNames[2] + './origin.jpg', SNP005)

    SNP01 = nr.SNP_Noise(lena, 0.1)
    cv2.imwrite( dirname + noiseImgNames[3] + './origin.jpg', SNP01)
imgs = [cv2.imread(dirname + filename + '/origin.jpg') for filename in noiseImgNames]

kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5,5))
kernel[0,0] = kernel[0,-1] = kernel[-1,0] = kernel[-1,-1] = 0



for i, img in enumerate(imgs):
    print(f'{noiseImgNames[i]}, SNR={nr.SNR(lena, img)}')

    img_box3 = nr.box_filter(img, size=3)
    cv2.imwrite( dirname +  noiseImgNames[i] + '/box3.jpg', img_box3)
    print(f'{noiseImgNames[i]} by box3, SNR={nr.SNR(lena,img_box3)}')

    img_box5 = nr.box_filter(img, size=5)
    cv2.imwrite( dirname +  noiseImgNames[i] + '/box5.jpg', img_box5)
    print(f'{noiseImgNames[i]} by box5, SNR={nr.SNR(lena,img_box5)}')

    img_med3 = nr.median_filter(img, size=3)
    cv2.imwrite( dirname +  noiseImgNames[i] + '/med3.jpg', img_med3)
    print(f'{noiseImgNames[i]} by med3, SNR={nr.SNR(lena,img_med3)}')

    img_med5 = nr.median_filter(img, size=5)
    cv2.imwrite( dirname +  noiseImgNames[i] + '/med5.jpg', img_med5)
    print(f'{noiseImgNames[i]} by med5, SNR={nr.SNR(lena,img_med5)}')

    img_opcl = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    img_opcl = cv2.morphologyEx(img_opcl, cv2.MORPH_CLOSE, kernel)
    cv2.imwrite( dirname +  noiseImgNames[i] + '/opcl.jpg', img_opcl)
    print(f'{noiseImgNames[i]} by opening-then-closing, SNR={nr.SNR(lena,img_opcl)}')

    img_clop = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    img_clop = cv2.morphologyEx(img_clop, cv2.MORPH_OPEN, kernel)
    cv2.imwrite( dirname +  noiseImgNames[i] + '/clop.jpg', img_clop)
    print(f'{noiseImgNames[i]} by closing-then-opening, SNR={nr.SNR(lena,img_clop)}')
