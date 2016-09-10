import numpy
import os.path

import Misc


# Number of nearest neighbours
nNearest = 6

# Minimum distance required between nearest neighbours
minDistance = 3

path = ""

fileNumber_len = 0
fileNumber_start = 0
fileNumber_end = 0


class ShankarCleanStable :
    
    def __init__(self, _path, _fileNumber_len, _fileNumber_start, _fileNumber_end) :
        
        global path, fileNumber_len, fileNumber_start, fileNumber_end
        
        path = _path
        
        fileNumber_len = _fileNumber_len
        fileNumber_start = _fileNumber_start
        fileNumber_end = _fileNumber_end
    
    
    def generateData(self) :
        
        with open(path + "/count_stable_cleaned.txt", "w") as f :
            
            f.write("#frame,count\n")
            
            for i in range (fileNumber_start, fileNumber_end) :
                
                fileName = Misc.getFileName(i, fileNumber_len)
                
                existence = os.path.isfile(path + "/position_stable/" + fileName + ".txt")
                
                print "ShankarCleanStable", path, fileName, existence
                
                if (not existence) :
    
                    continue
                    
                seeds = numpy.loadtxt(path + "/position_stable/" + fileName + ".txt", delimiter = ",", ndmin = 2)
                
                n = self.clean(fileName, seeds)
                
                s = str(i) + "," + str(n) + "\n"
                f.write(s)
                
                print "Count =", n
    
    
    def clean(self, fileName, seeds) :
        
        size = seeds.shape[0]
        
        nValid = 0
        
        if (not os.path.exists(path + "/position_stable_cleaned")) :
            
            os.makedirs(path + "/position_stable_cleaned")
        
        with open(path + "/position_stable_cleaned/" + fileName + ".txt", "w") as f :
            
            f.write("#x,y")
            
            for i in range (0, size) :
                
                # Exclude invalid points
                if (seeds[i, 0] == -1) :
                        
                    continue
                    
                for j in range (0, size) :
                    
                    # Skip over the same point and exclude invalid points
                    if (j == i or seeds[j, 0] == -1) :
                        
                        continue
                        
                    d = numpy.sqrt((seeds[i, 0] - seeds[j, 0])**2 + (seeds[i, 1] - seeds[j, 1])**2)
                    
                    if (d < minDistance) :
                        
                        comp = self.compare([i , j] , seeds)
                        
                        # Point i is valid
                        if (comp == 1) :
                            
                            # Mark point j as invalid
                            seeds[j, 0] = -1
                            seeds[j, 1] = -1
                            
                        # Point j is valid
                        elif (comp == 2) :
                            
                            # Mark point i as invalid
                            seeds[i, 0] = -1
                            seeds[i, 1] = -1
                            
                            # Add point j
                            s = str(seeds[j, 0]) + "," + str(seeds[j, 1]) + "\n"
                            f.write(s)
                            
                            nValid += 1
                            
                            break
                
                # Add point i
                if (seeds[i, 0] != -1) :
                    
                    s = str(seeds[i, 0]) + "," + str(seeds[i, 1]) + "\n"
                    f.write(s)
                    
                    nValid += 1
        
        return nValid
    
    
    def compare(self, r, seeds) :
        
        stdDev1 = numpy.std(self.getNearest(r[0], seeds, exclude = [r[1]]))
        stdDev2 = numpy.std(self.getNearest(r[1], seeds, exclude = [r[0]]))
        
        if (stdDev1 <= stdDev2) :
            
            return 1
            
        return 2
    
    
    def getNearest(self, r, seeds, exclude) :
        
        nSeeds = seeds.shape[0]
        
        nearest = numpy.array([])
        
        for i in range (0, nSeeds) :
            
            # Skip over the same point and exclude invalid points
            if (i == r or seeds[i, 0] == -1 or i in exclude) :
                
                continue
                
            d = numpy.sqrt((seeds[r, 0] - seeds[i, 0])**2 + (seeds[r, 1] - seeds[i, 1])**2)
            
            # Make sure distances from at least nNearest neighbours are stored
            if (nearest.size < nNearest) :
                
                nearest = numpy.append(nearest, [d])
                
                continue
                
            # If d < stored distance, replace that
            temp = [int(d < val) for val in nearest]
            
            if (not numpy.prod(temp)) :
                
                # Index of the first point that is more than d distance away
                index = numpy.array(numpy.where(temp == 0))
                
                if (index.size) :
                    
                    nearest[index[0, 0]] = d
               
        return nearest
