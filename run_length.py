import cv2 as cv
import numpy as np

def run_length(dataPath):
    ##Color image grayscale
    image = cv.imread(dataPath,1)
    grayimg = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    rows, cols = grayimg.shape

    image1 = grayimg.flatten() #Reduce the dimensionality of the grayscaled two-dimensional image to a one-dimensional list

    #Binarization operation
    for i in range(len(image1)): # goes through every pixel of image
        if image1[i] >= 127:
            image1[i] = 255
        if image1[i] < 127:
            image1[i] = 0


    data = []
    image3 = []
    count = 1
    #Stroke compression encoding
    for i in range(len(image1)-1):
        if (count == 1):
            image3.append(image1[i])
        if image1[i] == image1[i+1]:
            count = count + 1
            if i == len(image1) - 2:
                image3.append(image1[i])
                data.append(count)
        else:
            data.append(count)
            count = 1

    if(image1[len(image1)-1] != image1[-1]):
        image3.append(image1[len(image1)-1])
        data.append(1)

    #Stroke encoding and decoding
    rec_image = []
    for i in range(len(data)):
        for j in range(data[i]):
            rec_image.append(image3[i])

    rec_image = np.reshape(rec_image,(rows,cols))

    #cv.imshow('rec_image',rec_image) #Re-output the binarized image
    cv.imwrite('./rl_image.jpg', rec_image)
    cv.waitKey(0)