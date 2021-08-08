from PIL import Image as image
import sys
import cv2 as cv
import numpy as np



def encoding(dec, data):
    val = bin(dec)[:-1] + ("1" if data else "0")
    return int(val,2)

def decoding(dec):
    return 255 if int(bin(dec)[-1]) else 0


def encoding_pixel(color_cover, color_data):
    r = encoding(color_cover[0], color_data[0] if isinstance(color_data, tuple) else color_data)
    g = encoding(color_cover[1], color_data[1] if isinstance(color_data, tuple) else color_data)
    b = encoding(color_cover[2], color_data[2] if isinstance(color_data, tuple) else color_data)
    return r, g, b

def decoding_pixel(color_cover):
    return decoding(color_cover[0]), decoding(color_cover[1]), decoding(color_cover[2])

def insert(cover_img, data_img):
    if cover_img.size != data_img.size:
        raise ValueError("Image size is different")
    #dst = runlength 
    dst = image.new("RGB", cover_img.size, (0,0,0))
    width, height = cover_img.size
    pixels_cover = cover_img.load()
    pixels_dst = dst.load()
    pixels_data = data_img.load()
    for y in range(height):
        for x in range(width):
            color_cover = pixels_cover[x,y]
            color_data = pixels_data[x,y]
            encoding_pixel(color_cover, color_data)
            pixels_dst[x,y] = encoding_pixel(color_cover, color_data)
    return dst

def extract(cover):
    dst = image.new("RGB", cover.size, (0,0,0))
    width, height = cover.size
    pixels_dst = dst.load()
    pixels_cover = cover.load()
    for y in range(height):
        for x in range(width):
            color = pixels_cover[x,y]
            pixels_dst[x,y] = decoding_pixel(color)
    return dst

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

if __name__ == '__main__':
    if len(sys.argv) > 4 or len(sys.argv) < 3:
        print("Usage: " + sys.argv[0] +" is wrong." )
        print("type: team2_steg.py -h coverfile.jpg datafile.jpg or team2_steg.py -e encoded.png")
        sys.exit(1)

    basePath = './' # set the base path

    if sys.argv[1] == '-h': # if the option is -h, then hide
        print("start encoding" + sys.argv[2] + ' ' + sys.argv[3])
        coverPath = basePath+sys.argv[2] # cover file path
        cover = image.open(coverPath) # load cover image
        dataPath = basePath+sys.argv[3] # data file path
        run_length(dataPath) # rl encoding on data image
        data = image.open("./rl_image.jpg") # load data image
        # cover.show()
        # data.show()
        
        new_img = insert(cover,data)
        new_img.save("./encoded.png")
        # new_img.show()

    if sys.argv[1] == '-e': # if the option is -e, then extract
        print("start decoding" + sys.argv[2])
        newPath = basePath + sys.argv[2]
        new_img = image.open(newPath)
        decoding_img = extract(new_img)
        decoding_img.save("./decoded.png")
        print("decoding is done")
