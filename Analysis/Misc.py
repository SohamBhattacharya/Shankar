import math


# Add zeros to the beginning. Like, 1 -> 0001
def getFileName(fileNumber, fileNumber_len) :
    
    fileName = "Image"
    
    for j in range (0, fileNumber_len - len(str(fileNumber))) :
        
        fileName += "0"
        
    fileName += str(fileNumber)
    
    return fileName


# Arc length to linear frequency                                                  
def arcLengthToFrequency(length, exposure_time, radius) :
    
    freq = length / (2 * math.pi * radius * exposure_time)
    
    return freq
