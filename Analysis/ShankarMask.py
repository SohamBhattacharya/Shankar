import numpy
import os.path
import scipy.misc

import Misc


center_x = 540
center_y = 465

radius = 490

path = ""
path_static = ""

fileNumber_len = 0
fileNumber_start = 0
fileNumber_end = 0


class ShankarMask :
    
    def __init__(self, _path, _path_static, _fileNumber_len, _fileNumber_start, _fileNumber_end) :
        
        global path, path_static, fileNumber_len, fileNumber_start, fileNumber_end
        
        path = _path
        path_static = _path_static
        fileNumber_len = _fileNumber_len
        fileNumber_start = _fileNumber_start
        fileNumber_end = _fileNumber_end
    
    
    def generateData(self) :
        
        img = scipy.misc.imread(path_static + "/sudden stop.bmp")
        img_bg = scipy.misc.imread(path + "/bmp/" + Misc.getFileName(fileNumber_start, fileNumber_len) + ".bmp")
        
        img = self.subtract_background(img, img_bg)
        img = self.flatten_image(img)
        
        self.mask(img)
        
        scipy.misc.imsave(path_static + "/sudden stop_masked.png", img)
        
        if (not os.path.exists(path + "/masked")) :
            
            os.makedirs(path + "/masked")
        
        for i in range(fileNumber_start, fileNumber_end + 1) :
            
            fileName = Misc.getFileName(i, fileNumber_len)
            
            existence = os.path.isfile(path + "/bmp/" + fileName + ".bmp")
            
            print "ShankarMask", path, fileName, existence
            
            if (not existence) :
                
                continue
            
            img = scipy.misc.imread(path + "/bmp/" + fileName + ".bmp")
            
            img = self.subtract_background(img, img_bg)
            img = self.flatten_image(img)
            
            self.mask(img)
            
            scipy.misc.imsave(path + "/masked/" + fileName + ".png", img)
    
    
    def setPath(self, run) :
        
        global path
        
        path =  "run" + str(run) + "/" + location[run-1]
    
    
    def subtract_background(self, img, bg) :
        
        img = numpy.array(img, dtype = int)
        bg = numpy.array(bg, dtype = int)
        
        img = img - bg
        img[img < 0] = 0
        
        """imgShape = img.shape
        imgWidth = imgShape[1]
        imgHeight = imgShape[0]
        imgDepth = imgShape[2]
        
        img_sub = empty(imgShape)
        
        for i in range(0, imgHeight) :
            
            for j in range(0, imgWidth) :
                
                for k in range(0, imgDepth) :
                    
                    img_sub[i, j, k] = float(img[i, j, k]) - float(bg[i, j, k])
                    
                    if (img_sub[i, j, k] < 0) :
                        
                        img_sub[i, j, k] = 0"""
        
        return img
    
    
    def flatten_image(self, img) :
        
        img = numpy.array(img, dtype = int)
        
        """imgShape = img.shape
        imgWidth = imgShape[1]
        imgHeight = imgShape[0]
        
        img_flat = empty((imgHeight, imgWidth))
        
        for i in range(0, imgHeight) :
            
            for j in range(0, imgWidth) :
                
                img_flat[i, j] = average(img[i, j])"""
        
        return numpy.average(img, axis = 2)
    
    
    def mask(self, img) :
        
        imgShape = img.shape
        imgWidth = imgShape[1]
        imgHeight = imgShape[0]
	
        for i in range(0, imgHeight) :
            
            reachedMaskEdge = 0
            
            # From left
            for j in range(0, imgWidth) :
		
                d = numpy.sqrt((center_x - j)**2 + (center_y - i)**2)
                
                if (d < radius) :
                    
                    reachedMaskEdge = 1
                    
                    break
                    
                img[i, j] = 0
                
            if (not reachedMaskEdge) :
                
                continue
                
            # From right
            for j in reversed(range(0, imgWidth)) :
                
                d = numpy.sqrt((center_x - j)**2 + (center_y - i)**2)
                
                if (d < radius) :
                    
                    break
                    
                img[i, j] = 0

