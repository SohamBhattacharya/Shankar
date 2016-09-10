import numpy


path_total = ""
path = ""
zero_frame = 0
time_interval = 0

class ShankarScaleCount :
    
    
    def __init__(self, _path_total, _path, _zero_frame, _time_interval) :
        
        global path_total, path, zero_frame, time_interval
        
        path = _path
        path_total = _path_total
        
        zero_frame = _zero_frame
        time_interval = _time_interval
    
    
    def generateData(self) :
        
        with open(path + "/count_stable_cleaned_scaled.txt", "w") as f :
            
            f.write("#frame,time(s),fraction\n")
            
            nTotal = numpy.loadtxt(path_total + "/total_count.txt")
            data = numpy.loadtxt(path + "/count_stable_cleaned.txt", delimiter = ",")
            
            for i in range(0, data.shape[0]) :
                
                t = (data[i, 0] - zero_frame) * time_interval
                frac = float(data[i, 1] / nTotal)
                
                s = str(int(data[i, 0])) + "," + str(t) + "," + str(frac) + "\n"
                f.write(s)
