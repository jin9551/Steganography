from PIL import Image as image


def encoding(dec, data):
    val = bin(dec)[:-1] + ("1" if data else "0")
    return int(val,2)

def decoding(dec):
    return 255 if int(bin(dec)[-1]) else 0

# def rl_encoding:
# 
# 
# def rl_decoding:
#
#

def encoding_pixel(color_ori, color_data):
    r = encoding(color_ori[0], color_data[0] if isinstance(color_data, tuple) else color_data)
    g = encoding(color_ori[1], color_data[1] if isinstance(color_data, tuple) else color_data)
    b = encoding(color_ori[2], color_data[2] if isinstance(color_data, tuple) else color_data)
    return r, g, b

def decoding_pixel(color_ori):
    return decoding(color_ori[0]), decoding(color_ori[1]), decoding(color_ori[2])

def insert(ori_img, data_img):
    if ori_img.size != data_img.size:
        raise ValueError("Image size is different")
    #dst = runlength 
    dst = image.new("RGB", ori_img.size, (0,0,0))
    width, height = ori_img.size
    pixels_ori = ori_img.load()
    pixels_dst = dst.load()
    pixels_data = data_img.load()
    for y in range(height):
        for x in range(width):
            color_ori = pixels_ori[x,y]
            color_data = pixels_data[x,y]
            encoding_pixel(color_ori, color_data)
            pixels_dst[x,y] = encoding_pixel(color_ori, color_data)
    return dst

def extract(ori):
    dst = image.new("RGB", ori.size, (0,0,0))
    width, height = ori.size
    pixels_dst = dst.load()
    pixels_ori = ori.load()
    for y in range(height):
        for x in range(width):
            color = pixels_ori[x,y]
            pixels_dst[x,y] = decoding_pixel(color)
    return dst

if __name__ == '__main__':
    ori = image.open("./dog.jpg")
    data = image.open("./hidden.jpg")
    ori.show()
    data.show()
    input("press and start encoding")
    new_img = insert(ori,data)
    new_img.save("./encodig.png")
    new_img.show()
    input("encoding is done\npress and start decoding")
    decoding_img = extract(new_img)
    #rl_decoding
    decoding_img.show()
    decoding_img.save("./decoding.png")
    input("decoding is done")
