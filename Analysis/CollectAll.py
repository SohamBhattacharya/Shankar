from numpy import *
from Queue import Queue


path = ""
directory = "/media/soham/E/ShankarData"
directory_cool = array(["run1_5vto2.2v", "run2_5vto2.4v", "run3_5vto2.55v", "run4_5vto2.6v", "run5_5vto2.7v", \
                        "run6_5vto2.85v", "run7_5vto3v", "run8_5vto3.2v", "run9_5vto3.35v", "run10_5vto3.45v", \
                        "run11_5vto3.6v", "run12_5vto3.8v", "run13_5vto3.7v", "run14_5vto3.95v", "run15_5vto4.1v", \
                        "run16_5vto4.25v", "run17_5vto4.15v"])
                        
voltage_cool = array([2.2, 2.4, 2.55, 2.6, 2.7, \
                      2.85, 3, 3.2, 3.35, 3.45, \
                      3.6, 3.8, 3.7, 3.9, 4.1, 
                      4.25, 4.15])

nRuns = directory_cool.size


class CollectAll :
    
    def main(self) :
        
        with open("all.txt", "w") as f :
        
            f.write("#run\t" + "#voltage_cool\t" + "#arc_length\t" + "#total_count\t" + "#clustered_count" + "\n")
            
            for i in range (0, nRuns) :
                
                self.setPath(i + 1)
                
                arr = array([str(i+1), str(voltage_cool[i])])
                
                with open(path + "/avg_arc_length.txt", "r") as g:
                    
                    for line in g :
                        
                        words = line.split("\t")
                        
                        # str(float()) removes the "\n" from the end of the word
                        arr = append(arr, str(float(words[0])))
                        
                with open(directory + "/run" + str(i+1) + "/total_count.txt", "r") as g:
                    
                    for line in g :
                        
                        words = line.split("\t")
                        arr = append(arr, str(float(words[0])))
                        
                with open(path + "/count_stable_cleaned.txt", "r") as g:
                    
                    line = ""
                    
                    q = Queue()
                    
                    for line in g :
                        
                        words = line.split("\t")
                        q.put(float(words[1]))
                        
                        if (q.qsize() > 10) :
                            
                            q.get()
                            
                    arr = append(arr, str(int(round(average(q.queue)))))
                    
                s = "\t".join(arr)
                s += "\n"
                f.write(s)
                
                print "run", i + 1, arr
    
    
    def setPath(self, run) :
        
        global path
        
        path =  directory + "/run" + str(run) + "/" + directory_cool[run-1]
    
    
r = CollectAll()
r.main()
