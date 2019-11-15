from Pixel import Pixel
from struct import pack, iter_unpack
import math

def rasterToBMPData(raster):
    raster = raster[::-1]
    # RBG is 24 bits
    if(raster[0][0].length == 3):
        bitsize = 24
    #RGBA is 32 bits
    elif raster[0][0].length == 4:
        bitsize = 32

    paddingneeded = math.ceil(((bitsize * len(raster[0])) / 32) * 4) % 4

    output = b''
    for row in raster:
        for pixel in row:
            if(pixel.length == 3):
                output += pack('<BBB', pixel.blue, pixel.green, pixel.red)
            else:
                output += pack('<BBBB', pixel.blue, pixel.green, pixel.red, pixel.alpha)
        for i in range(paddingneeded):
            output += b'\x00'

    return output

def BMPDataToRaster(imagedata, rowsize, paddingPerRow, compressionMethodDict, compressionMethod):
    rows = []
    j = 0
    for i in range(rowsize + paddingPerRow, len(imagedata) + 1, rowsize + paddingPerRow):
        rows.append(imagedata[j:i])
        j = i

    pixelrows = []
    for index, row in enumerate(rows):
        inner = []
        for item in iter_unpack('c' * len(compressionMethodDict[compressionMethod]), row[0:len(row) - paddingPerRow]):
            inner.append(Pixel(item))
        pixelrows.append(inner)

    #Flip the rows because BMPs read bottom-top
    return pixelrows[::-1]
