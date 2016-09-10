import math
import numpy
import os.path
import scipy.misc

import Misc


path = ""

fileNumber_len = 0
fileNumber_start = 0
fileNumber_end = 0

nAvg = 20


class ShankarArcLength :
    
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
        
        with open(path + "/arc_length.txt", "w") as f1, \
            open(path + "/arc_length_average.txt", "w") as f2:
            
            f1.write("#frame,arc_length\n")
            f2.write("#arc_length_average\n")
            
            arr_arc_length = numpy.empty(0)
            
            for i in range (fileNumber_start, fileNumber_end + 1) :
                
                fileName = Misc.getFileName(i, fileNumber_len)
                
                existence = os.path.isfile(path + "/arc/" + fileName + ".png")
                
                print "ShankarGetArc", path, fileName, existence
                
                if (not existence) :
                    
                    continue
                
                img = scipy.misc.imread(path + "/arc/" + fileName + ".png")
                
                imgShape = img.shape
                imgWidth = imgShape[1]
                imgHeight = imgShape[0]
                
                data = numpy.empty((0, 2))
                
                for r in range(0, imgHeight) :
                    
                    for c in range(0, imgWidth) :
                        
                        if (img[r, c]) :
                            
                            data = numpy.append(data, [[c, r]], axis = 0)
                
                # Nearest point on the circle
                data_nearest = numpy.empty((0, 2))
                
                for j in range(0, data.shape[0]) :
                    
                    l = numpy.sqrt((data[j, 0]-x_center)**2 + (data[j, 1]-y_center)**2)
                    
                    nearest_x = x_center + radius/l*(data[j, 0] - x_center)
                    nearest_y = y_center + radius/l*(data[j, 1] - y_center)
                    
                    data_nearest = numpy.append(data_nearest, [[nearest_x, nearest_y]], axis = 0)
                
                arc_length = 0
                
                # Calculate length of arc
                for j in range(0, data_nearest.shape[0]) :
                    
                    for k in range(j + 1, data_nearest.shape[0]) :
                        
                        d = numpy.sqrt((data_nearest[j, 0]-data_nearest[k, 0])**2 + (data_nearest[j, 1]-data_nearest[k, 1])**2) / 2.0
                        
                        if (d > radius) :
                            
                            continue
                        
                        ang = math.pi - 2*math.acos(d/radius)
                        l = radius * ang
                        
                        if (l > arc_length) :
                            
                            arc_length = l
                
                arr_arc_length = numpy.append(arr_arc_length, arc_length)
                
                s = str(i) + "," + str(arc_length) + "\n"
                f1.write(s)
                
                print "Arc length =", arc_length
            
            arc_length_avg = numpy.average(arr_arc_length[-nAvg:])
            
            s = str(arc_length_avg) + "\n"
            f2.write(s)
            
            print "Average arc length =", arc_length_avg

