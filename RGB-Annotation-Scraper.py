# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 13:21:37 2020
- a script that scrapes bounding box (BB) annotaions from a directory of annotated images
- takes an image and loads it into a multidimensional pixel array
- looks for indices in the array where the RGB format color of the BB is seen
- here, the color is yellow (255,255,0)
- finds the first and last yellow pixel in the picture
- does a little math to determine which pixel is l and t, and then what w and h are for the BB.
"""

import numpy as np
import imageio
import os
import pandas as pd
import glob
import math


class Batch_Results:
    
    def __init__(self):
    
            self.jpgDF = ""
    
    def createJPGdataframe(self,jpgDF=""):
        
        directoryName = "D:\ResearchProjects\Learning Machine Learning\Making an MTurk dataset\scripts (annotation retrieval)/"
        row_count=1
        fileCount = len(glob.glob1(directoryName,"*B_annotated.png"))
        
        column_names = ["inputImageName", "x_res", "y_res", "l", "t", "w", "h", "agree"]
        jpgDF = pd.DataFrame(columns = column_names)
        print(jpgDF)
        
        for path, dirs, files in os.walk(directoryName):    
            for filename in files:
                if "B_annotated" in filename:
                    
                    arr = imageio.imread(([filename])[0], as_gray=False, pilmode="RGB")
                    indices = []
                    
                    print("Now processing image " + str(row_count) + " of " + str(fileCount))
                   
                    for i in range(0,arr.shape[0]):
                        for k in range(0,arr.shape[1]):
                            if np.all(np.asarray(arr[i,k])==np.asarray([255,255,0])):
                                indices.append([i,k])
                                
                                # print("the first and last indices are: ")
                                # print(indices[0], indices[-1])
                                
                    if len(indices) != 0:            
                        l = indices[0][1]
                        t = indices[0][0]
                        w = indices[-1][1]-indices[0][1]
                        h = indices[-1][0]-indices[0][0]
                    else:
                        l = math.nan
                        t = math.nan
                        w = math.nan
                        h = math.nan
                    
                    # append everything
                    jpgDF = jpgDF.append({'inputImageName': [filename],
                                             'x_res': imageio.imread(directoryName + ([filename])[0]).shape[1],
                                             'y_res': imageio.imread(directoryName + ([filename])[0]).shape[0],
                                             'l': l,
                                             't': t,
                                             'w': w,
                                             'h': h
                                             }, ignore_index=True)
        
                    row_count = row_count+1
        
        print("")            
        print(jpgDF)
        print("")
        
        jpgDF.to_csv('image_list.csv', sep=';', encoding='utf-8')
        
        print("Results written to .csv at: " + str(directoryName) + "image_list.csv")

results = Batch_Results()  
results.createJPGdataframe()
