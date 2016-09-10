import math
import numpy
import os.path
import scipy.misc

import Misc


path = ""

fileNumber_len = 0
fileNumber_start = 0
fileNumber_end = 0

# points located at distance > dist_threshold from the radius are noise
dist_threshold = 5

class ShankarCorrectArc :
    
    def __init__(self, _path, _fileNumber_len, _fileNumber_start, _fileNumber_end) :
        
        global path, fileNumber_len, fileNumber_start, fileNumber_end
        
        path = _path
        
        fileNumber_len = _fileNumber_len
        fileNumber_start = _fileNumber_start
        fileNumber_end = _fileNumber_end
    
    
    def generateData(self) :
        
        arc_circle_fit_data = numpy.loadtxt(path + "/arc_circle_fit_parameters.txt", delimiter = ",")
        
        x_center = arc_circle_fit_data[0]
        y_center = arc_circle_fit_data[1]
        radius = arc_circle_fit_data[2]
        
        # Correct arc circle
        img = scipy.misc.imread(path + "/arc_circle.png")
        img = self.removeNoise(img, x_center, y_center, radius)
        scipy.misc.imsave(path + "/arc_circle_corrected.png", img)
        
        # Correct individual arcs
        for i in range (fileNumber_start, fileNumber_end + 1) :
        
            fileName = Misc.getFileName(i, fileNumber_len)
            
            existence = os.path.isfile(path + "/arc/" + fileName + ".png")
            
            print "ShankarCorrectArc", path, fileName, existence
            
            if (not existence) :
                
                continue
            
            img = scipy.misc.imread(path + "/arc/" + fileName + ".png")
            img = self.removeNoise(img, x_center, y_center, radius)
            scipy.misc.imsave(path + "/arc/" + fileName + ".png", img)
    
    
    def removeNoise(self, img, x, y, rad) :
        
        for r in range(0, img.shape[0]) :
            
            for c in range(0, img.shape[1]) :
                
                d = numpy.sqrt((r-y)**2 + (c-x)**2)
                
                if ((d - rad) > dist_threshold) :
                    
                    img[r, c] = 0
        
        return img
