import numpy
import os.path
import scipy.misc
import scipy.optimize


path = ""
image_name = ""

class ShankarFitArcCircle :
    
    def __init__(self, _path, _image_name) :
        
        global path, image_name
        
        path = _path
        image_name = _image_name
    
    
    def generateData(self) :
        
        with open(path + "/arc_circle_fit_parameters.txt", "w") as f :
            
            img = scipy.misc.imread(path + "/" + image_name)
            
            imgShape = img.shape
            imgWidth = imgShape[1]
            imgHeight = imgShape[0]
            
            data = numpy.empty((0, 2))
            
            for r in range(0, imgHeight) :
                
                for c in range(0, imgWidth) :
                    
                    if (img[r, c]) :
                        
                        data = numpy.append(data, [[c, r]], axis = 0)
            
            center_estimate = (imgWidth/2.0, imgHeight/2.0)
            center, err = scipy.optimize.leastsq(self.getDeviation, center_estimate, args = (data[:, 0], data[:, 1]))
            radius = self.getDistFromCenter(center[0], center[1], data[:, 0], data[:, 1]).mean()
            
            s = "#x_center,y_center,radius" + "\n"
            f.write(s)
            
            s = str(center[0]) + "," + str(center[1]) + "," + str(radius) + "\n"
            f.write(s)
            
            print path
            print "x =", center[0], "y =", center[1], "radius =", radius
    
    
    def getDistFromCenter(self, x_center, y_center, x, y) :
        
        return numpy.sqrt((x-x_center)**2 + (y-y_center)**2)
   
    
    def getDeviation(self, center, x, y):
       
       d = self.getDistFromCenter(center[0], center[1], x, y)
       
       return d - d.mean()
