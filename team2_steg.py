from PIL import Image as image
import sys
import cv2 as cv
import numpy as np


# Team 2 
# Jinha Jeong
# Chaeju Kim
# Alex Smith

def encoding(dec, data):
    val = bin(dec)[:-1] + ("1" if data else "0")   # the binary of color value either 1 or 0
    return int(val,2)

def decoding(dec):
    return 255 if int(bin(dec)[-1]) else 0 # the binary of color value either 255 or 0/ black or white 

# it depends on the cover image but pixel of an image has 3 color components rgb
# for each color component we are going to use lsb of it
def encoding_pixel(color_cover, color_data):
    r = encoding(color_cover[0], color_data[0] if isinstance(color_data, tuple) else color_data) # encoding for the red component / if color_data datatype is tuple then use color_data[0] else use color_data
    g = encoding(color_cover[1], color_data[1] if isinstance(color_data, tuple) else color_data) # encoding for the green component
    b = encoding(color_cover[2], color_data[2] if isinstance(color_data, tuple) else color_data) # encoding for the blue component
    return r, g, b

# decode
def decoding_pixel(color_cover):
    return decoding(color_cover[0]), decoding(color_cover[1]), decoding(color_cover[2]) # decode for each color component r, g, b

def insert(cover_img, data_img):
    if cover_img.size != data_img.size: # if the cover image size is not equal to the message image size then raise Value Error
        raise ValueError("Image size is different")
    ############### the datatype for rgb becomes tuple here!!!!!!!!!!!
    dst = image.new("RGB", cover_img.size, (0,0,0)) # initialize the new image(stego image) that has size equal to the cover image, but color is in black 
    width, height = cover_img.size # width and height is also equal to the cover image
    pixels_cover = cover_img.load() # load the cover image
    pixels_dst = dst.load()  # load the stego image
    pixels_data = data_img.load() # load the message image
    # call pixels one by one and encode them.
    for y in range(height):
        for x in range(width):
            color_cover = pixels_cover[x,y] # one pixel from cover
            color_data = pixels_data[x,y] # one pixel from data
            pixels_dst[x,y] = encoding_pixel(color_cover, color_data) # put them in the stego image after encode data in the cover
    return dst # return the stego image

def extract(cover):
    dst = image.new("RGB", cover.size, (0,0,0))  # initialize the new image(recovered image) that has size equal to the cover image, but color is in black 
    width, height = cover.size # width and height is also equal to the cover image
    pixels_dst = dst.load() # load the recovered image
    pixels_cover = cover.load() # load the stego image
    # call pixels one by one and encode them.
    for y in range(height):
        for x in range(width):
            color = pixels_cover[x,y] # one pixel from the stego image
            pixels_dst[x,y] = decoding_pixel(color) # decode the pixel and put it on the recovered image
    return dst

# run length encoding of a given data file
def run_length(dataPath):
    ## Color image grayscale
    image = cv.imread(dataPath,1) # read image using opencv
    grayimg = cv.cvtColor(image, cv.COLOR_BGR2GRAY) # with that image we are turning into a gray color image
    rows, cols = grayimg.shape
    flattened = grayimg.flatten() #Reduce the dimensionality of the grayscaled two-dimensional image to a one-dimensional list

    #Binarization operation
    for i in range(len(flattened)): # goes through every pixel of image
        if flattened[i] >= 127: # if the color of the pixel is bigger than 127 then set it white
            flattened[i] = 255
        if flattened[i] < 127: # if the color of the pixel is smaller than 127 then set it black 
            flattened[i] = 0

    data = [] # initiallizing the data
    rl_image = [] # preparing for rl_image
    count = 1 # initiallizing the count
    #rl compression encoding
    for i in range(len(flattened)-1): #goes through every pixel of flattened image
        if (count == 1): # if the count == 1
            rl_image.append(flattened[i]) # apeend it to the rl_image for the run length encoding
        if flattened[i] == flattened[i+1]: # if the next pixel has the same value as the current value
            count = count + 1 # increment the cout
            if i == len(flattened) - 2: # if the pixel is not the end of the flattened image
                rl_image.append(flattened[i]) # then append it to the rl_image
                data.append(count) # append the count 
                # so it becmoes like 255,3; 0,4; 255, 1; 0,10; ... etc. 
        else:
            data.append(count) # if the value doesn't continue make the count = 1
            count = 1 # sort of resetting

    if(flattened[len(flattened)-1] != flattened[-1]):
        rl_image.append(flattened[len(flattened)-1])
        data.append(1)
    # run length decode
    rec_image = [] # preparing for recovered image
    # goes through every pixels in rl_image
    for i in range(len(data)):
        for j in range(data[i]):
            rec_image.append(rl_image[i])

    # reshape the [.................] to [[....],[......]... etc] so that we can make it into image
    rec_image = np.reshape(rec_image,(rows,cols)) # reshape it to rows X cols
    
    #cv.imshow('rec_image',rec_image) #check if the image is right
    cv.imwrite('./rl_image.jpg', rec_image) # save the binary image for the further use 
    cv.waitKey(0)

if __name__ == '__main__':
    # check if the command line has correct number of parameters 
    # len 4 for the encoding
    # len 3 for the decoding
    if len(sys.argv) > 4 or len(sys.argv) < 3: 
        print("Usage: " + sys.argv[0] +" is wrong." )
        print("type: team2_steg.py -h coverfile.jpg datafile.jpg or team2_steg.py -e encoded.png")
        sys.exit(1)

    basePath = './' # set the base path

    if sys.argv[1] == '-h': # if the option is -h, then hide
        print("start encoding " + sys.argv[2] + ' ' + sys.argv[3])
        coverPath = basePath+sys.argv[2] # cover file path
        cover = image.open(coverPath) # load cover image
        dataPath = basePath+sys.argv[3] # data file path
        run_length(dataPath) # rl encoding on data image
        data = image.open("./rl_image.jpg") # load data image
        # cover.show()
        # data.show()
        
        new_img = insert(cover,data) # call encoding function
        new_img.save("./encoded.png") # save the encoded image
        # new_img.show()

    if sys.argv[1] == '-e': # if the option is -e, then extract
        print("start decoding" + sys.argv[2])
        newPath = basePath + sys.argv[2] # set the path for the stego image
        new_img = image.open(newPath) # load the stego image
        decoding_img = extract(new_img) # call extracting function
        decoding_img.save("./decoded.png") # save the result in the current directory
        print("decoding is done")
