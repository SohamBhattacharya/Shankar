import numpy

from ShankarArcLength import ShankarArcLength
from ShankarArcLengthToFrequency import ShankarArcLengthToFrequency
from ShankarCleanStable import ShankarCleanStable
from ShankarCorrectArc import ShankarCorrectArc
from ShankarCount import ShankarCount
from ShankarFitArcCircle import ShankarFitArcCircle
from ShankarFitGrowth import ShankarFitGrowth
from ShankarGetArc import ShankarGetArc
from ShankarMask import ShankarMask
from ShankarScaleCount import ShankarScaleCount
from ShankarStable import ShankarStable
from ShankarTotalCount import ShankarTotalCount
from ShankarVoronoi import ShankarVoronoi


fileNumber_len = 4
nRuns = 17

fileNumber_start = numpy.array([ \
    569, 786, 2250, 4754, 6468, \
    8637, 9943, 10671, 11673, 13834, \
    15091, 19070, 26234, 28577, 27410, \
    29560, 32007])
    
fileNumber_end = numpy.array([ \
    671, 1759, 3011, 5585, 7112, \
    9477, 10545, 11516, 12502, 14966, \
    15875, 22001, 26939, 29358, 28160, \
    29955, 32708])

threshold = numpy.zeros(nRuns)
threshold[0: 5] = 140
threshold[5:] = 190

zero_frame = numpy.array([ \
    599, 1070, 2490, 5214, 6665, \
    9171, 10242, 10966, 12068, 14313, \
    15411, 19793, 26572, 29156, 27821, \
    29753, 32191])

exposure_time = numpy.zeros(nRuns)
exposure_time[0: 5] = 1.0/30
exposure_time[5:] = 1.0/21

time_interval = numpy.zeros(nRuns)
time_interval[0: 5] = 10
time_interval[5:] = 1

path = ""
directory = "/media/soham/E/ShankarData"
directory_cool = numpy.array([ \
    "run1_5vto2.2v", "run2_5vto2.4v", "run3_5vto2.55v", "run4_5vto2.6v", "run5_5vto2.7v", \
    "run6_5vto2.85v", "run7_5vto3v", "run8_5vto3.2v", "run9_5vto3.35v", "run10_5vto3.45v", \
    "run11_5vto3.6v", "run12_5vto3.8v", "run13_5vto3.7v", "run14_5vto3.95v", "run15_5vto4.1v", \
    "run16_5vto4.25v", "run17_5vto4.15v"])


class RunAll :
    
    def main(self) :
        
        for i in range(0, 4) :
            
            self.setPath(i + 1)
            
            
            
            # Mask and subtract background
            print "\n", "run", i + 1, "********** ShankarMask **********"
            s = ShankarMask(path, directory + "/run" + str(i+1), fileNumber_len, fileNumber_start[i], fileNumber_end[i])
            s.generateData()
            
            
            
            # Get particle details
            print "\n", "run", i + 1, "********** ShankarTotalCount **********"
            s = ShankarTotalCount(directory + "/run" + str(i+1), threshold[i], fileNumber_len, fileNumber_start[i], fileNumber_end[i])
            s.generateData()
            
            print "\n", "run", i + 1, "********** ShankarCount **********"
            s = ShankarCount(path, threshold[i], fileNumber_len, fileNumber_start[i], fileNumber_end[i])
            s.generateData()
            
            print "\n", "run", i + 1, "********** ShankarStable **********"
            s = ShankarStable(path, fileNumber_len, fileNumber_start[i], fileNumber_end[i])
            s.generateData()
            
            print "\n", "run", i + 1, "********** ShankarCleanStable **********"
            s = ShankarCleanStable(path, fileNumber_len, fileNumber_start[i], fileNumber_end[i])
            s.generateData()
            
            
            
            # Scale and fit growth curve
            print "\n", "run", i + 1, "********** ShankarScaleCount **********"
            s = ShankarScaleCount(directory + "/run" + str(i+1), path, zero_frame[i], time_interval[i])
            s.generateData()
            
            print "\n", "run", i + 1, "********** ShankarFitGrowth **********"
            s = ShankarFitGrowth(path)
            s.generateData()
            
            
            
            # Get arc details
            print "\n", "run", i + 1, "********** ShankarGetArc **********"
            s = ShankarGetArc(path, fileNumber_len, fileNumber_start[i], fileNumber_end[i])
            s.generateData()
            
            print "\n", "run", i + 1, "********** ShankarFitArcCircle **********"
            s = ShankarFitArcCircle(path, "arc_circle.png")
            s.generateData()
            
            print "\n", "run", i + 1, "********** ShankarCorrectArc **********"
            s = ShankarCorrectArc(path, fileNumber_len, fileNumber_start[i], fileNumber_end[i], )
            s.generateData()
            
            print "\n", "run", i + 1, "********** ShankarFitArcCircle **********"
            s = ShankarFitArcCircle(path, "arc_circle_corrected.png")
            s.generateData()
            
            print "\n", "run", i + 1, "********** ShankarArcLength **********"
            s = ShankarArcLength(path, fileNumber_len, fileNumber_start[i], fileNumber_end[i])
            s.generateData()
            
            print "\n", "run", i + 1, "********** ShankarArcLengthToFrequency **********"
            s = ShankarArcLengthToFrequency(path, exposure_time[i])
            s.generateData()
            
            
            
            #print "\n", "run", i + 1, "********** ShankarVoronoi **********"
            #s = ShankarVoronoi(path, fileNumber_len, fileNumber_start[i], fileNumber_end[i])
            #s.generateData()
    
    
    def setPath(self, run) :
        
        global path
        
        path =  directory + "/run" + str(run) + "/" + directory_cool[run-1]
    
    
r = RunAll()
r.main()
