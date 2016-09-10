import numpy
import scipy.optimize


path = ""


class ShankarFitGrowth :
    
    def __init__(self, _path) :
        
        global path
        
        path = _path
    
    
    def generateData(self) :
        
        data = numpy.loadtxt(path + "/count_stable_cleaned_scaled.txt", delimiter = ",")
        
        start = numpy.where(data[:, 1] == 0)[0][0]
        
        par, cov = scipy.optimize.curve_fit( \
            self.fitFunction, data[start:, 1], data[start:, 2])
        
        with open(path + "/growth_fit_parameters.txt", "w") as f :
            
            f.write("#Fitting function: frac(t) = frac_sat*(1-exp(-t/tau))\n")
            f.write("#frac_sat,tau\n")
            
            s = str(par[0]) + "," + str(par[1]) + "\n"
            f.write(s)
            
            print "frac_sat =", par[0], "tau =", par[1]
    
    
    def fitFunction(self, t, frac_sat, tau) :
        
        return frac_sat * (1 - numpy.exp(-t/tau))
