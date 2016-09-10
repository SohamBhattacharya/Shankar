import numpy
import os.path
import scipy.misc

import Misc


# Region around maxima
delta = 2

# Region to scan
x1 = 1070
y1 = 170

x2 = 1279#-1
y2 = 400

r_threshold = 150
gb_threshold = 120

path = ""

fileNumber_len = 0
fileNumber_start = 0
fileNumber_end = 0


class ShankarGetArc :
    
    def __init__(self, _path, _fileNumber_len, _fileNumber_start, _fileNumber_end) :
        
        global path, fileNumber_len, fileNumber_start, fileNumber_end
        
        path = _path
        
        fileNumber_len = _fileNumber_len
        fileNumber_start = _fileNumber_start
        fileNumber_end = _fileNumber_end
    
    
    def generateData(self) :
        
        if (not os.path.exists(path + "/arc")) :
            
            os.makedirs(path + "/arc")
        
        scanWidth = x2-x1
        scanHeight = y2-y1
        
        imgCircle = numpy.zeros((scanHeight, scanWidth))
        
        for i in range (fileNumber_start, fileNumber_end + 1) :
            
            fileName = Misc.getFileName(i, fileNumber_len)
            
            existence = os.path.isfile(path + "/bmp/" + fileName + ".bmp")
            
            print "ShankarGetArc", path, fileName, existence
            
            if (not existence) :
                
                continue
            
            img = scipy.misc.imread(path + "/bmp/" + fileName + ".bmp")
            img = img[y1: y2+1, x1: x2+1, :]
            
            #imgShape = img.shape
            #imgWidth = imgShape[1]
            #imgHeight = imgShape[0]
            
            imgArc = numpy.zeros((scanHeight, scanWidth))
            
            # Duplicate array
            for r in range (0, scanHeight) :
                
                for c in range (0, scanWidth) :
                    
                    if (img[r, c, 0] > r_threshold and img[r, c, 1] < gb_threshold and img[r, c, 2] < gb_threshold) :
                        
                        imgArc[r, c] = 1
                        imgCircle[r, c] = 1
            
            scipy.misc.imsave(path + "/arc/" + fileName + ".png", imgArc)
            
        scipy.misc.imsave(path + "/arc_circle.png", imgCircle)
    
    
    def scannableArea(self, imgShape) :
        
        global x1, y1, x2, y2
        
        if (x1 == -1) :
            
            x1 = 0
            
        if (y1 == -1) :
            
            y1 = 0
            
        if (x2 == -1) :
            
            x2 = imgShape[1] - 1
            
        if (y2 == -1) :
            
            y2 = imgShape[0] - 1
