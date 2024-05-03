from PIL import Image
import subprocess
from colorama import Fore, Style

ASCII_CHARS = "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
MAX_PIXEL_VALUE = 255

def get_pixel_matrix(img, height):
    img.thumbnail((height, 200))
    pixels = list(img.getdata())
    return [pixels[i:i+img.width] for i in range(0, len(pixels), img.width)]

def get_intensity_matrix(pixels_matrix, algo_name='average'):
    intensity_matrix = []
    for row in pixels_matrix:
        intensity_row = []
        for p in row:
            if algo_name == 'average':
                intensity = (p[0] + p[1] + p[2] / 3.0)
            elif algo_name == 'max_min':
                intensity = (max(p) + min(p) / 2.0)
            elif algo_name == 'luminosity':
                intensity = 0.21*p[0] + 0.72*p[1] + 0.07*p[2]
            else:
                raise Exception("Unrecognixed algo_name: %s" % algo_name)

            intensity_row.append(intensity)
        intensity_matrix.append(intensity_row)

    return intensity_matrix

def normalize_intensity_matrix(intensity_matrix):
    normalized_intensity_matrix = []
    max_pixel = max(map(max, intensity_matrix))
    min_pixel = min(map(min, intensity_matrix))
    for row in intensity_matrix:
        rescaled_row = []
        for p in row:
            r = MAX_PIXEL_VALUE * (p - min_pixel) / float(max_pixel - min_pixel)
            rescaled_row.append(r)
        normalized_intensity_matrix.append(rescaled_row)

    return normalized_intensity_matrix

def invert_intensity_matrix(intensity_matrix):
    inverted_intensity_matrix = []
    for row in intensity_matrix:
        inverted_row = []
        for p in row:
            inverted_row.append(MAX_PIXEL_VALUE - p)
        inverted_intensity_matrix.append(inverted_row)

    return inverted_intensity_matrix

def convert_to_ascii(intensity_matrix, ascii_chars):
    ascii_matrix = []
    for row in intensity_matrix:
        ascii_row = []
        for p in row:
            ascii_row.append(ascii_chars[int(p/MAX_PIXEL_VALUE * len(ascii_chars)) - 1])
        ascii_matrix.append(ascii_row)

    return ascii_matrix

def print_ascii_matrix(ascii_matrix, text_color):
    for row in ascii_matrix:
        line = [p+p+p for p in row]
        print(text_color + "".join(line))

    print(Style.RESET_ALL)

filepath = "ascii-pineapple.jpg"
# subprocess.call(["imagesnap", filepath, "-w", "2"])

img = Image.open(filepath)
pixels = get_pixel_matrix(img, 1000)

intensity_matrix = get_intensity_matrix(pixels, 'luminosity')
intensity_matrix = normalize_intensity_matrix(intensity_matrix)
#intensity_matrix = invert_intensity_matrix(intensity_matrix)
#intensity_matrix = invert_intensity_matrix(intensity_matrix)

ascii_matrix = convert_to_ascii(intensity_matrix, ASCII_CHARS)
print_ascii_matrix(ascii_matrix, Fore.GREEN)










# from PIL import Image
# import  numpy as np

# im = Image.open("ascii-pineapple.jpg")

# print (im.size)
# pixel_matrix=np.array(im) 

# for i in range(len(pixel_matrix)):
#     for j in range(len(pixel_matrix[i])):
#         pixel=(pixel_matrix[i][j]).mean()
#         ascii_char = ''.join(map(chr, [int(pixel)]))
#         print (ascii_char,end="")
        

          

         


