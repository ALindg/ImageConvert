import struct
"""
Class written for bitmap pixels.
:param pixeldata: Must be a tuple of RGB or RGBA hex values
"""
class Pixel:
    def __init__(self, pixeldata):
        if type(pixeldata[0]) is int:
            if(len(pixeldata) == 4):
                self.alpha = pixeldata[3]
            self.red = pixeldata[2]
            self.green = pixeldata[1]
            self.blue = pixeldata[0]
            self.length = 3 if len(pixeldata) != 4 else 4
            self.data = [self.red, self.green, self.blue] if self.length != 4 else \
                [self.red, self.green, self.blue, self.alpha]
            return
        if(len(pixeldata) == 4):
            self.alpha = int.from_bytes(struct.unpack('c', pixeldata[3])[0], "little")
            self.red = int.from_bytes(struct.unpack('c', pixeldata[2])[0], "little")
            self.green = int.from_bytes(struct.unpack('c', pixeldata[1])[0], "little")
            self.blue = int.from_bytes(struct.unpack('c', pixeldata[0])[0], "little")
            self.data = [self.red, self.green, self.blue, self.alpha]
            self.length = 4
        else:
            self.alpha = -1
            self.red = int.from_bytes(struct.unpack('c', pixeldata[2])[0], "little")
            self.green = int.from_bytes(struct.unpack('c', pixeldata[1])[0], "little")
            self.blue = int.from_bytes(struct.unpack('c', pixeldata[0])[0], "little")
            self.data = [self.red, self.green, self.blue]
            self.length = 3

    def toBytes(self):
        data = bytes(self.data)
        return data

    def __repr__(self):
        return "Pixel(%s)" % ",".join([str(i) for i in self.data])

    def __str__(self):
        return "(%s)" % ",".join([str(i) for i in self.data])
