import numpy
import Queue # Be careful with multithreading when using things like q.qsize() or q.queue

import os.path

import Misc


# No. of images to "average" over
# Must be odd
qSize = 5

# Points separated by more than this will be considered to be separate points
# That is, over qSize images, the variation of a seed by this amount is allowed
variation = 2.5 #sqrt(8)

path = ""

fileNumber_len = 0
fileNumber_start = 0
fileNumber_end = 0


class ShankarStable :
    
    def __init__(self, _path, _fileNumber_len, _fileNumber_start, _fileNumber_end) :
        
        global path, fileNumber_len, fileNumber_start, fileNumber_end
        
        path = _path
        
        fileNumber_len = _fileNumber_len
        fileNumber_start = _fileNumber_start
        fileNumber_end = _fileNumber_end
    
    
    def generateData(self) :
        
        q = Queue.Queue()
        qFileNumber = Queue.Queue()
        qFileName = Queue.Queue()
        
        with open(path + "/count_stable.txt", "w") as f :
            
            f.write("#frame,count\n")
            
            for i in range (fileNumber_start, fileNumber_end + 1) :
                
                fileName = Misc.getFileName(i, fileNumber_len)
                
                existence = os.path.isfile(path + "/position/" + fileName + ".txt")
                
                print "ShankarStable", path, fileName, existence
                
                if (not existence) :
                    
                    continue
                        
                q.put(numpy.loadtxt(path + "/position/" + fileName + ".txt", delimiter = ",", ndmin = 2))
                qFileNumber.put(i)
                qFileName.put(fileName)
                
                if (q.qsize() == qSize) :
                    
                    # Number and name of the file that is being modified
                    fileNumber_mod = qFileNumber.queue[int(qSize / 2)]
                    fileName_mod = qFileName.queue[int(qSize / 2)]
                    
                    nStable = self.getStablePositions(fileName_mod, self.duplicateQueue(q))
                    
                    s = str(fileNumber_mod) + "," + str(nStable) + "\n"
                    f.write(s)
                    
                    # Feedback: The central image in the queue is now the modified one
                    #print q.queue[int(qSize / 2)].shape
                    q.queue[int(qSize / 2)] = numpy.loadtxt(path + "/position_stable/" + fileName_mod + ".txt", delimiter = ",", ndmin = 2)
                    #print q.queue[int(qSize / 2)].shape
                    
                    print "Count =", nStable
                    
                    q.get()
                    qFileNumber.get()
                    qFileName.get()
    
    
    def duplicateQueue(self, q) :
        
        q_temp = Queue.Queue()
        
        for i in range (0, qSize) :
            
            temp = numpy.copy(q.queue[i])
            q_temp.put(temp)
            
        return q_temp
    
    
    def getStablePositions(self, fileName, q) :
        
        nStable = 0
        
        if (not os.path.exists(path + "/position_stable")) :
            
            os.makedirs(path + "/position_stable")
        
        with open(path + "/position_stable/" + fileName + ".txt", "w") as f:
            
            f.write("#x,y\n")
            
            # Select a file
            for i in range (0, qSize) :
                
                # Select a seed from that file
                for j in range (0, q.queue[i].shape[0]) :
                    
                    if (q.queue[i][j, 0] == -1) :
                        
                        continue
                    
                    tally = numpy.zeros(qSize)
                    
                    tally[i] = 1
                    
                    avg_x = q.queue[i][j, 0]
                    avg_y = q.queue[i][j, 1]
                    
                    # Check if that seed is present in the rest of the files
                    for k in range (0, qSize) :
                        
                        if (k == i) :
                            
                            continue
                        
                        temp = self.seedMatch(q.queue[i][j, 0], q.queue[i][j, 1], q.queue[k])
                        
                        tally[k] = temp[0]
                        
                        if (temp[0]) :
                            
                            avg_x += q.queue[k][temp[1], 0]
                            avg_y += q.queue[k][temp[1], 1]
                            
                            q.queue[k][temp[1], 0] = -1
                            q.queue[k][temp[1], 1] = -1
                            
                    q.queue[i][j, 0] = -1
                    q.queue[i][j, 1] = -1
                    
                    # If seed is present in more than half the files, then include it
                    n = sum(tally)
                    
                    if (n > int(qSize / 2)) :
                        
                        avg_x = float(avg_x) / n
                        avg_y = float(avg_y) / n
                        
                        s = str(avg_x) + "," + str(avg_y) + "\n"
                        f.write(s)
                        
                        nStable += 1
                        
        return nStable
        
    
    def seedMatch(self, x, y, seeds) :
        
        for i in range (0, seeds.shape[0]) :
            
            d = numpy.sqrt((x - seeds[i, 0])**2.0 + (y - seeds[i, 1])**2.0)
            
            if (d <= variation) :
                
                return [1, i]
                
        return [0, -1]
