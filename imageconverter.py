from PIL import Image
import os
import sys

def save_as(imagepath, extension):
	extension = input("What file type extension will it be?")
    image = Image.open(imagepath)
    imagepath = imagepath[:imagepath.rindex(".")]
    newpath ="%s\%s.%s" % (os.path.dirname(os.path.realpath(imagepath)), imagepath, extension)

    image.save(newpath)
    print(newpath)

def save_whole_directory(directory, extension):
    exit()

with open("c:\\users\\lindg\\desktop\\imageconverter\\output.txt", "w") as f:
	f.write(sys.argv[0])
save_as(sys.argv[0])

