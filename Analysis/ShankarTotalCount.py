import numpy
import os.path
import scipy.misc


delta = 2

# Region to be analyzed
x1 = 0
y1 = 0

x2 = 0
y2 = 0

path = ""

threshold = 0

fileNumber_len = 0
fileNumber_start = 0
fileNumber_end = 0


class ShankarTotalCount :
    
    def __init__(self, _path, _threshold, _fileNumber_len, _fileNumber_start, _fileNumber_end) :
        
        global path, threshold, fileNumber_len, fileNumber_start, fileNumber_end
        
        path = _path
        
        threshold = _threshold
        
        fileNumber_len = _fileNumber_len
        fileNumber_start = _fileNumber_start
        fileNumber_end = _fileNumber_end
    
    
    def generateData(self) :
        
        with open(path + "/total_count.txt", "w") as f:
            
            f.write("#total_count\n")
            
            img = scipy.misc.imread(path + "/sudden stop_masked.png")
            
            nMax = self.findLocalMaxima(img)
            
            f.write(str(nMax) + "\n")
            
            print "Total count =", nMax
    
    
    def findLocalMaxima(self, img) :
        
        imgShape = img.shape
        imgWidth = imgShape[1]
        imgHeight = imgShape[0]
	
        imgAnal = numpy.zeros((imgHeight, imgWidth, 2))
        
        rowStart = 0 + delta #y1 + delta
        rowEnd = imgHeight - delta -1 #y2 - delta
        
        colStart = 0 + delta #x1 + delta
        colEnd = imgWidth - delta -1 #x2 - delta
        
        nMax = 0
	
        for i in range (rowStart, rowEnd + 1) :
            
            for j in range (colStart, colEnd + 1) :
		
                imgAnal[i, j, 0] = img[i, j]
		
        with open(path + "/position_all.txt", "w") as f :
			
            f.write("#x,y\n") #,value\n")
            
            for i in range (rowStart, rowEnd + 1) :
				
                for j in range (colStart, colEnd + 1) :
				
                    if (imgAnal[i, j, 0] >= threshold and imgAnal[i, j, 1] == 0 and self.isLocalMaximum(i, j, imgAnal, recursive = 1)) :
			
                        imgAnal[i, j, 1] = 1
			
                        nMax += 1
			
                        s = str(j) + "," + str(i) + "\n" # + "," + str(imgAnal[i, j, 0]) + "\n"
			
                        f.write(s)
        
        return nMax
    
    
    def isLocalMaximum(self, row, col, imgAnal, recursive) :
	
        for i in range(row - delta, row + delta + 1) :
	    
            for j in range(col - delta, col + delta + 1) :
		
                if (i == row and j == col) :
                    
                    continue
		    
                if ((imgAnal[i, j, 0] > imgAnal[row, col, 0] and recursive and not self.isLocalMaximum(i, j, imgAnal, recursive = 0)) or imgAnal[i, j, 1] == 1) :
                
                    return 0
		    
        return 1
