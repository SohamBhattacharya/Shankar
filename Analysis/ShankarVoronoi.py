from numpy import *
from scipy import misc
from matplotlib import pyplot
from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import Polygon

import os.path

import Misc


path = ""

fileNumber_len = 0
fileNumber_start = 0
fileNumber_end = 0

scale = 5


class ShankarVoronoi :
    
    def __init__(self, _path, _fileNumber_len, _fileNumber_start, _fileNumber_end) :
        
        global path, fileNumber_len, fileNumber_start, fileNumber_end
        
        path = _path
        
        fileNumber_len = _fileNumber_len
        fileNumber_start = _fileNumber_start
        fileNumber_end = _fileNumber_end
    
    
    def generateData(self) :
        
        if (not os.path.exists(path + "/voronoi")) :
            
            os.makedirs(path + "/voronoi")
        
        for i in range (fileNumber_start, fileNumber_end) :
            
            fileName = Misc.getFileName(i, fileNumber_len)
            
            existence = os.path.isfile(path + "/position_stable_cleaned/" + fileName + ".txt")
            
            print "ShankarVoronoi", path, fileName, existence
            
            if (not existence) :
  
                continue
                
            seeds = self.getSeeds(path + "/position_stable_cleaned/" + fileName + ".txt")
            
            # Check if there are at least 4 points
            if (seeds.shape[0] < 4) :
                
                continue
                
            vor = Voronoi(seeds)
            
            for region in vor.regions :
                
                # check if region is closed and not empty (Voronoi.regions returns an empty array at the beginning)
                if (-1 not in region and region) :
                    
                    polyVertices = array([[vor.vertices[i][0], vor.vertices[i][1]] for i in region])
                    poly = Polygon(polyVertices)
                    area = poly.area
                    
                    threshold = 30
                    
                    area = area if area <= threshold else threshold
                    
                    edges = polyVertices.shape[0]
                    
                    if (edges <= 4) :
                        
                        cellColor = (0, 0, 0)
                        
                    elif (edges == 5) :
                        
                        cellColor = (1, 0, 0)
                        
                    elif (edges == 6) :
                        
                        cellColor = (0, 1, 0)
                        
                    elif (edges == 7) :
                        
                        cellColor = (0, 0, 1)
                        
                    else :
                        
                        cellColor = (1, 1, 1)
                    
                    # Fill cells
                    pyplot.fill(*zip(*polyVertices), color = cellColor, alpha = 0.5)
                    # Draw cell borders
                    pyplot.plot(*zip(*polyVertices), linewidth = 0.1, color = "0")
                    # Plot the seeds
                    pyplot.plot(*zip(*seeds), marker = "o", markersize = 1, linestyle = "")
            
            #DPI = pyplot.gcf().get_dpi()
            
            pyplot.xlim(0, 1279)
            pyplot.ylim(0, 959)
            pyplot.gca().invert_yaxis()
            pyplot.gca().set_aspect("equal", adjustable = "box")
            
            #pyplot.show()
            pyplot.savefig(path + "/voronoi/" + fileName + ".eps", format = "eps")
            
            pyplot.close()
    
    
    def getSeeds(self, fileName) :
        
        seeds = zeros((0, 2))
	
        with open(fileName, "r") as f:
            
            for line in f:
            
                words = line.split("\t")
                seeds = append(seeds, [[float(words[0]), float(words[1])]], axis = 0)
        
        return seeds
