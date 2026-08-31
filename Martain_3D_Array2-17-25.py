import numpy as np
import torch
import pickle
import pandas as pd
import os

"""x_max = 20
y_max = 20
z_max = 15
AltResoultion = 50

# Sources Data File and Creates file where data is output.
# Must have Topography_tensors folder to work
inputfilename = input("Enter name of data file to be converted. ")

filePath = os.getcwd() + "/Topography_Tensors/"""

def createTensor(x_max, y_max, z_max, AltResolution, file):
    filePath = os.getcwd() + "/Topography_Tensors/"
    resultFileName = file[0:-4] + "-"+ str(x_max) +"x"+str(y_max)+'x'+str(z_max) + " " + str(AltResolution) + "(m)"
    resultFile = open(filePath + resultFileName, "ab")

    # Read specific columns from CSV file
    dataFolderPath = os.getcwd() + "/dataFiles/"
    columns = ['center_lon', 'center_lat', 'average_topography']
    coordinateInfo = pd.read_csv(dataFolderPath+file, usecols=columns)

    # Finding Min and Max to create an evenly shaped grid.

    # First .iloc searches for a row in the csv file
    # The second .iloc takes a data value, 0 = longitude, 1= latitude, 2 = altitude 
    longMin = coordinateInfo.iloc[0].iloc[0]
    longMax = coordinateInfo.iloc[-1].iloc[0]
    print(longMax)

    latMin = coordinateInfo.iloc[0].iloc[1]
    latMax = coordinateInfo.iloc[0].iloc[1]

    altMin =coordinateInfo.iloc[0].iloc[2]
    altMax =coordinateInfo.iloc[0].iloc[2]

    for i in range(0,len(coordinateInfo), 1):
        latTemp = coordinateInfo.iloc[i].iloc[1]
        altTemp = coordinateInfo.iloc[i].iloc[2]
        if latTemp < latMin:
            latMin = latTemp
        if latTemp > latMax:
            latMax = latTemp

        if altTemp < altMin:
            altMin = altTemp
        if altTemp > altMax:
            altMax = altTemp

    latStep = (latMax-latMin)/x_max

    longStep = (longMax-longMin)/y_max

    print (altMax-altMin)
    altStep = AltResolution

    #if altStep*z_max < longMax-longMin:
    #    print("Warning resolution too high data will be lost. Increase dimensions or decrease resolution")

    if latStep< longStep:
        longStep=latStep
    elif longStep <= latStep:
        latStep=longStep

    # Before the tensor is created, the data is loaded into a 3D array.
    # The array starts as full, when conditions are not met the element is set to 0.

    topography_array = np.array([[[0]*x_max]*y_max]*z_max)

    for x in range(0,x_max):
        ThresholdLong = longMin+longStep*x
        ThresholdLong = round(ThresholdLong, 2)

        for y in range(0,y_max):
            ThresholdLat = latMin+latStep*y
            ThresholdLat = round(ThresholdLat, 2)
        
            for i in range(len(coordinateInfo)):
                TempLat = coordinateInfo.iloc[i].iloc[1]
                TempLong = coordinateInfo.iloc[i].iloc[0]
                TempAlt = coordinateInfo.iloc[i].iloc[2]
                if (ThresholdLat < TempLat and TempLat < ThresholdLat+latStep) and (ThresholdLong < TempLong and TempLong < ThresholdLong+longStep):
                    for z in range(0,z_max):
                        ThresholdAlt = altMin+altStep*(z)
                        if TempAlt < ThresholdAlt:
                            topography_array[x][y][z] = 1
                    
        
        
            


        



    topography_tensor = torch.tensor(topography_array)

    del topography_array

    pickle.dump(topography_tensor, resultFile)

    print(topography_tensor)
    return topography_tensor
