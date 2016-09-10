import numpy
import os.path
import scipy.misc

import Misc


# Region around maxima
delta = 2

path = ""

threshold = 0

fileNumber_len = 0
fileNumber_start = 0
fileNumber_end = 0


class ShankarCount :
    
    def __init__(self, _path, _threshold, _fileNumber_len, _fileNumber_start, _fileNumber_end) :
        
        global path, threshold, fileNumber_len, fileNumber_start, fileNumber_end
        
        path = _path
        
        threshold = _threshold
        
        fileNumber_len = _fileNumber_len
        fileNumber_start = _fileNumber_start
        fileNumber_end = _fileNumber_end
    
    
    def generateData(self) :
        
        with open(path + "/count.txt", "w") as f :
            
            f.write("#frame,count\n")
            
            for i in range (fileNumber_start, fileNumber_end + 1) :
                
                fileName = Misc.getFileName(i, fileNumber_len)
                
                existence = os.path.isfile(path + "/masked/" + fileName + ".png")
                
                print "ShankarCount", path, fileName, existence
                
                if (not existence) :
                    
                    continue
                
                img = scipy.misc.imread(path + "/masked/" + fileName + ".png")
                
                imgShape = img.shape
                imgWidth = imgShape[1]
                imgHeight = imgShape[0]
                
                imgAnal = numpy.zeros((imgHeight, imgWidth, 2))
                
                # Duplicate array
                for r in range (0, imgHeight) :
                    
                    for c in range (0, imgWidth) :
                        
                        imgAnal[r, c, 0] = img[r, c]
                
                nMax = self.findLocalMaxima(fileName, imgAnal)
                
                s = str(i) + "," + str(nMax) + "\n"
                f.write(s)
                
                print "Count =", nMax
    
    
    def findLocalMaxima(self, fileName, imgAnal) :
        
        rowStart = 0 + delta
        rowEnd = imgAnal.shape[0] - delta
        
        colStart = 0 + delta
        colEnd = imgAnal.shape[1] - delta
        
        nMax = 0
	
        if (not os.path.exists(path + "/position")) :
            
            os.makedirs(path + "/position")
        
        with open(path + "/position/" + fileName + ".txt", "w") as f:
			
            f.write("#x,y\n") #,value\n")
            
            for i in range (rowStart, rowEnd) :
				
                for j in range (colStart, colEnd) :
				
                    if (imgAnal[i, j, 0] >= threshold and imgAnal[i, j, 1] == 0 and self.isLocalMaximum(i, j, imgAnal, recursive = 1)) :
			
                        imgAnal[i, j, 1] = 1
			
                        nMax += 1
			
                        s = str(j) + "," + str(i) + "\n" # + "," + str(imgAnal[i, j, 0]) + "\n"
                        f.write(s)
			
        return nMax
    
    
    def isLocalMaximum(self, row, col, imgAnal, recursive) :
	
        for i in range(row - delta, row + delta + 1) :
	    
            if (i >= imgAnal.shape[0]) :
                
                break
                
            for j in range(col - delta, col + delta + 1) :
		
                if (i == row and j == col) :
                    
                    continue
                    
                if (j == imgAnal.shape[1]) :
                    
                    break
		    
                condition = self.isLocalMaximum(i, j, imgAnal, recursive = 0) if recursive else 1
                
                if ((imgAnal[i, j, 0] > imgAnal[row, col, 0] and condition) or imgAnal[i, j, 1] == 1) :
                
                    return 0
                
                """if ((imgAnal[i, j, 0] > imgAnal[row, col, 0] and recursive and self.isLocalMaximum(i, j, imgAnal, recursive = 0)) or imgAnal[i, j, 1] == 1) :
                
                    return 0"""
                    
                """if (imgAnal[i, j, 0] > imgAnal[row, col, 0] or imgAnal[i, j, 1] == 1) :
                
                    return 0"""
		    
        return 1
