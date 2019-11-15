import struct
import math
from Pixel import Pixel
from bitmapraster import rasterToBMPData
from bitmapraster import BMPDataToRaster

#Take a singular 4 byte hex number, turn it into an int
def hexToInt(hex):
    if(len(hex) == 2):
        return struct.unpack('h', hex)[0]
    if(len(hex) == 4):
        return struct.unpack("i", hex)[0]

compressionMethod = {0: "RGB",
                     1: "RLE8",
                     2: "RLE4",
                     3: "RGBA",
                     4: "JPG",
                     5: "PNG",
                     6: "RGBA Bit Fields",
                     11: "CMYK",
                     12: "CMYKRLE8",
                     13: "CYMKRLE4"}


def pixelToTuple(hex):
    return struct.unpack("ccc", hex)

class bmpFile:
    def __init__(self, file=-1):
        try:
            if(file == -1):
                # If it's an empty constructor, set all fields to none for default
                fields = ['file', 'fileHeader', 'header',
                          'headerSize', 'width', 'height', 'planes',
                          'bitsPerPixel',
                          'compressionMethod', 'imagesize', 'hrez', 'vrez',
                          'palettenumcolors', 'importantolorsnum', 'imagedata',
                          'rowsize', 'paddingPerRow']

                self.items = {k: None for k in fields}
                return
            #If it wasn't default, try to open the file
            file = open(file, 'rb').read()
        except IOError:
            raise IOError("Could not find file! " + file + " is not a valid file in this directory.")

            
        # Gather the relevant data we need. Insofar, there has been no need for extra information
        # Besides what is located within the header and information data. 
        # Should there be a need for additional info, changes should be made to this class
        # Which reflects that need for any additional info from the file being required.
        self.items = {}
        self.items['file'] = file
        self.items['fileHeader'] = self.file[0:14]
        self.items['size'] = hexToInt(self.fileHeader[2:6])
        self.items['dataStartAddress'] = hexToInt(self.fileHeader[10:14])
        headersize = hexToInt(self.file[14:18])
        self.items['header'] = self.file[14:headersize+14]

        # Unpack all values from the header into a tuple
        headerItems = struct.unpack('IIIHHIIIIII', (self.header[:40]))
        # Make a list of the fields we'll use for more items in the dict
        fields = ['headerSize', 'width', 'height', 'planes', 'bitsPerPixel',
                  'compressionMethod', 'imagesize', 'hrez', 'vrez',
                  'palettenumcolors', 'importantolorsnum']
        # Zip all the fields and items together in a dictionary,
        # then update our items dictionary.
        self.items.update({k: v for (k,v) in zip(fields, headerItems)})

        self.items['imagedata'] = self.file[self.dataStartAddress: self.dataStartAddress + self.imagesize]
        self.items['rowsize'] = self.getRowSize()
        self.items['paddingPerRow'] = self.rowsize % 4
        # Validate the file header and other checks before use
        self.validate()
        # If it validated, we can get a raster of it
        self.items['raster'] = self.getRaster()
    
    def validate(self):
        if self.fileHeader[:2] != b"BM":
            raise IOError("File header is not BM, invalid file.")
        if self.size != len(self.file):
            raise IOError("Size does not match calculated size. Invalid file.")


    def getRaster(self):
        if(compressionMethod[self.compressionMethod] in ["RGB", "RGBA"]):
            return BMPDataToRaster(self.imagedata, self.getRowSize(), self.paddingPerRow, compressionMethod, self.compressionMethod)
        raise IOError("Unimplimented compression method. Got %s" % self.compressionMethod)

    def __getattr__(self, item):
        return self.items[item]

    def __str__(self):
        output = "BMP Image with data:\n"
        for k, v in self.items.items():
            output += k + ": " + str(v) + "\n"
        return output

    def getRowSize(self):
        return math.ceil(((self.bitsPerPixel * self.width) / 32) * 4)

    def write(self, location):
        fileHeader = b'BM'
        size = 14 + 40 + len(self.imagedata)
        reserved = b'\x00\x00\x00\x00'
        dataStart = 14 + 40
        fileHeader += struct.pack('I', size)
        fileHeader += reserved
        fileHeader += struct.pack('I', dataStart)

        if(len(fileHeader) != 14):
            raise IOError("File header length was not 14, instead got %d" % len(fileHeader))


        DIBSize = 40
        width = self.width
        height = self.height
        planes = 1
        bitsPerPixel = self.bitsPerPixel
        compressionMethod = self.compressionMethod
        imageSize = len(self.imagedata)
        hrez = self.hrez
        vrez = self.vrez
        palettenumcolors = self.palettenumcolors
        importantcolorsnum = self.importantolorsnum

        DIBHeader = struct.pack('IIIHHIIIIII', DIBSize, width, height, planes, bitsPerPixel, compressionMethod, imageSize, hrez, vrez, palettenumcolors, importantcolorsnum)

        file = fileHeader + DIBHeader + self.imagedata
        f = open(location, 'wb')
        f.write(file)
        f.close()

# Testing / Debug purposes.
# These should respectively each print as an empty file and testimg.bmp
# testimg.bmp is a bmp file with exactly four pixels. 
# One red pixel, one green pixel, then on the second row: One blue pixel, one white pixel.
# It is 24 bits in bit depth and only has RGB values. 
#x = bmpFile()
#y = bmpFile("testimg.bmp")

#print(x)
#print(y)
