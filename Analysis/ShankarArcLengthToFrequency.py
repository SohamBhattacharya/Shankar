import numpy

import Misc


path = ""
exposure_time = 0


class ShankarArcLengthToFrequency :
    
    def __init__(self, _path, _exposure_time) :
        
        global path, exposure_time
        
        path = _path
        
        exposure_time = _exposure_time
    
    
    def generateData(self) :
        
        radius = numpy.loadtxt(path + "/arc_circle_fit_parameters.txt", delimiter = ",")[2]
        
        with open(path + "/frequency.txt", "w") as f:
            
            f.write("#frame,frequency(Hz)\n")
            
            data = numpy.loadtxt(path + "/arc_length.txt", delimiter = ",")
            
            for i in range(0, data.shape[0]) :
                
                freq = Misc.arcLengthToFrequency(data[i, 1], exposure_time, radius)
                s = str(int(data[i, 0])) + "," + str(freq) + "\n"
                f.write(s)
        
        with open(path + "/frequency_average.txt", "w") as f :
            
            length = numpy.loadtxt(path + "/arc_length_average.txt")
            
            f.write("#frequency_average(Hz)\n")
            
            freq = Misc.arcLengthToFrequency(length, exposure_time, radius)
            s = str(freq) + "\n"
            f.write(s)
            
            print "Average frequency =", freq
    
    
    def fitFunction(self, t, frac_sat, tau) :
        
        return frac_sat * (1 - numpy.exp(-t/tau))
