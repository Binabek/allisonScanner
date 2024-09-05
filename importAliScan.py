#
#    import function for Allison scanner data
#    John Wieland
###############################################################################

import re
import numpy as np

# Imports raw alison scanner data, no conversions included
def importRaw(fn):
    #search for slice headers, and pull metadata from file
    f = open(fn,"r")
    
    sliceArr = []
    for i,line in enumerate(f):
        if re.match("Slice\s[0-9]{3}",line):
            sliceArr.append(i)
        elif re.match("Angle\sStart",line):
            angIni = float(line.split(",")[-1])
        elif re.match("Angle\sStop",line):
            angFin = float(line.split(",")[-1])
        elif re.match("Angle\sDelta",line):
            angDel = float(line.split(",")[-1])
        elif re.match("Position\sStart",line):
            posIni = float(line.split(",")[-1])
        elif re.match("Position\sStop",line):
            posFin = float(line.split(",")[-1])
        elif re.match("Position\sDelta",line):
            posDel = float(line.split(",")[-1])
        elif re.match("Number\sBins",line):
            binN = int(float(line.split(",")[-1]))
    
    f.close()


    #construct arrays of positional and angle data
    #assuming angle is in milliradians
    angArr = np.arange(angIni,angFin+angDel/2,angDel)*1e-3
    posArr = -np.arange(posIni,posFin+posDel/2,posDel)
    
    #store number of position and agular sample points for slicing
    angN = angArr.shape[0]
    posN = posArr.shape[0]

    #extract data from csv, slice index by slice index
    #depends on the exact format of the outuput file
    #if output changes this whole read operation needs to change
    fullDat = np.zeros([binN,angN,posN])
    
    for i,s in enumerate(sliceArr):
        fullDat[i] = -np.genfromtxt(fn,delimiter=",",usecols=np.arange(1,posN+1),max_rows=angN,skip_header=s+14)

    return(fullDat,posArr,angArr)