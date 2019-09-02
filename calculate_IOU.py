# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 14:31:15 2019

Author: Rohit Malyala

Intended for: - analysis of Worker annotations from MTurk;
              - validation of responses compared to Expert annotations;
              - and visualization of these results.

Uses a non-geometric, near-exact method of assessing intersection/union
between Worker and Expert annotations of multiple bounding-boxes.
Labeled areas (with n boxes) are represented as 2d pixel arrays, then 
compared to each other for binary agreement per-pixel or per-array index value.

Calculations are approximate as pixel array sizes is minimized by 100 (variable).
i.e. an image of resolution 3100*3100 is represented as a 310*310 array.
If image resolutions are sufficently small this may be fixed later.

Loops through every HIT in an MTurk batch_results[xxxx].csv download. For 
every HIT with a viable expert annotation, the agreement between worker
and expert is written into the csv.

Currently unsure of what format precisely the Expert annotations will be 
loaded in, so I assume for now they are identical to the MTurk annotations.
That half of the parsing method can be changed later.

"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import re


class Batch_Results:

    def __init__(self, csv_filename="batch_results.csv"):

        self.csv_filename = csv_filename
        # self.c_image = ""
        self.scale_factor = ""
        self.war_int_array = ""
        self.ear_int_array = ""
        self.tr_array = ""
        self.ex_array = ""
        self.agreement = ""


    def csv_to_dataframe(self, csv_filename = "batch_results.csv"):

        self.batch_results = pd.read_csv(\
            self.csv_filename,\
                usecols=[\
                        'Input.image_url',\
                        'Answer.annotatedResult.boundingBoxes',\
                        'Answer.annotatedResult.inputImageProperties.height',\
                        'Answer.annotatedResult.inputImageProperties.width',\
                        'expertAnswer'])
        
        self.batch_results.columns=['URL','tr_results','y_res','x_res','ex_results']
        return self.batch_results


    def downscale_factor_select(self, scale_input=10):

        if int(scale_input)>0:
            self.scale_factor = scale_input
        else:
            print('Input out of bounds. Downscale factor set to 10')
            self.scale_factor = 10
        return self.scale_factor


    def parse_dataframe(self, c_image):
    
        # c_image is the row index for the HIT. 1 and 4 are column index for the strings with the lists of label data.
        worker_assignment_raw = self.batch_results.iloc[c_image,1]
        expert_assignment_raw = self.batch_results.iloc[c_image,4]

        print(worker_assignment_raw)
        print(expert_assignment_raw)

        # --------- WORKER -----------
        
        # Removes all extra characters except pixel integers in string
        replace = {'"label":"Stone",': "", "{": "", "}": "", '"height":' : "", '"left":' : "", '"top":' : "", '"width":' : "", '[' : "", ']' : ""}
        replace = dict((re.escape(k), v) for k, v in replace.items())
        pattern = re.compile("|".join(replace.keys()))
        war_str_list = pattern.sub(lambda m: replace[re.escape(m.group(0))], worker_assignment_raw)
    
        # convert comma-delimited string list to list of integers
        war_int_list = war_str_list.split(",")
        war_int_list = [int(i) for i in war_int_list]
        war_int_array = np.asarray(war_int_list)
        self.war_int_array = war_int_array.reshape(len(war_int_array)//4, 4)
    
        # --------- EXPERT -----------
    
        # Remove all extra characters except pixel integers in string
        replace = {'"label":"Stone",': "", "{": "", "}": "", '"height":' : "", '"left":' : "", '"top":' : "", '"width":' : "", '[' : "", ']' : ""}
        replace = dict((re.escape(k), v) for k, v in replace.items())
        pattern = re.compile("|".join(replace.keys()))
        ear_str_list = pattern.sub(lambda m: replace[re.escape(m.group(0))], expert_assignment_raw)
    
        # convert comma-delimited string list to list of integers
        ear_int_list = ear_str_list.split(",")
        ear_int_list = [int(i) for i in ear_int_list]
        ear_int_array = np.asarray(ear_int_list)
        self.ear_int_array = ear_int_array.reshape(len(ear_int_array)//4, 4)
    
        return self.war_int_array
        return self.ear_int_array
    


    def make_binary_2D_array(self):
       
        # create an array for a given image URL of length x*y resolution
        # starting at the top left point, get x.res
        print(str(self.scale_factor))
        x_res = int(self.batch_results.iloc[c_image,3]/self.scale_factor)
        y_res = int(self.batch_results.iloc[c_image,2]/self.scale_factor)
    
        
        # --------- WORKER -----------
        
        # build numpy array of zeros
        self.tr_array = np.zeros((x_res,y_res), dtype=int)
        
        for n_row in range(0,len(self.war_int_array)):
        
            h_tr = int(round(self.war_int_array[n_row,0]/self.scale_factor))
            l_tr = int(round(self.war_int_array[n_row,1]/self.scale_factor))
            t_tr = int(round(self.war_int_array[n_row,2]/self.scale_factor))
            w_tr = int(round(self.war_int_array[n_row,3]/self.scale_factor))
    
            # converts bounding box covered pixels to 1's 
            self.tr_array[t_tr:(t_tr+h_tr),l_tr:(l_tr+w_tr)] = 1
            # print("Just finished digitizing row number: " + str(n_row))
    
        # uncomment to visualize worker annotations in a spreadsheet!
        # np.savetxt("arrayvis_worker.csv", tr_array, delimiter=",")
        # print("Created visualization of worker annotation.")

        # --------- EXPERT -----------
            
        # build numpy array of zeros
        self.ex_array = np.zeros((x_res,y_res), dtype=int)
        
        for n_row in range(0,len(self.ear_int_array)):
        
            h_tr = int(round(self.ear_int_array[n_row,0]/self.scale_factor))
            l_tr = int(round(self.ear_int_array[n_row,1]/self.scale_factor))
            t_tr = int(round(self.ear_int_array[n_row,2]/self.scale_factor))
            w_tr = int(round(self.ear_int_array[n_row,3]/self.scale_factor))
            
            # converts bounding box covered pixels to 1's 
            self.ex_array[t_tr:(t_tr+h_tr),l_tr:(l_tr+w_tr)] = 1
            # print("Just finished digitizing row number: " + str(n_row))
    
        return self.tr_array
        return self.ex_array


    def calculate_IOU(self):
        
        if len(self.tr_array) == len(self.ex_array) and len(self.tr_array[1]) == len(self.ex_array[1]):

            overlap = np.array(self.tr_array * self.ex_array, dtype=bool)
            union   = np.array(self.tr_array + self.ex_array, dtype=bool)

            self.agreement = overlap.sum() / float(union.sum()) * 100
            
            print("")
            print('Intersection over union result:')
            print("% "+str(round(self.agreement,2)))
            print("")
            
            # fill in the agreement
            f = open(self.csv_filename, 'r', newline = '')
            reader = csv.reader(f)
            mylist = list(reader)
            f.close()
            mylist[(c_image+1)][34] = round(self.agreement,2)
            
            new_batch_results = open(self.csv_filename, 'w', newline = '')
            csv_writer = csv.writer(new_batch_results)
            csv_writer.writerows(mylist)
            new_batch_results.close()
            
            print("Agreement (IOU and %) written to batch_results.csv")
        
        else:
            print("Ensure image resolutions (and array sizes) are identical.")
            print("")

        return self.agreement
        
        
        
    def visualize_annotations(self, c_image):
        
        intersect_array = (self.tr_array) + (self.ex_array)
    
        figure, axarr = plt.subplots(1,3,"row")
        figure.suptitle('Intersection visual for csv index: '+\
                        str(c_image+1) + ". Agreement: " +str(round(self.agreement,2))+\
                        '\n HIT ID: ' + '36U4VBVNQP9ZYQ5ZG9NVHQTEO9SRUV',\
                        size=13, y=0.88)
        plt.tight_layout()
        
        axarr[0].imshow(self.tr_array)
        axarr[0].title.set_text('Worker labelling')
        
        axarr[1].imshow(self.ex_array)
        axarr[1].title.set_text('Expert labelling')
        
        axarr[2].imshow(intersect_array)
        axarr[2].title.set_text('Intersection/Union')
        
        return


# Looping through all the functions for each index.


results = Batch_Results("batch_results.csv")

results.csv_to_dataframe()
results.downscale_factor_select(1)
row_count = len(result.batch_results.index)-1

for c_image in range(0,int(row_count)):

    print(c_image)
    results.parse_dataframe(c_image)
    results.make_binary_2D_array()
    results.calculate_IOU()
    results.visualize_annotations(c_image)


