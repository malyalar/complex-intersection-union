# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 14:31:15 2019

@author: Rohit Malyala

Intended for: - analysis of Worker annotations from MTurk;
              - validation of responses compared to Expert annotations;
              - and visualization of these results.

Uses a non-geometric, near-exact method of assessing intersection/union
between Worker and Expert annotations of multiple bounding-boxes.
Labeled areas (with n boxes) are represented as 2d pixel arrays,
reshaped to 1d arrays, then compared to each other for binary agreement
at a per-pixel (or per element-in-array) level.

Calculations are approximate as pixel arrays size is minimized by 100.
i.e. an image of resolution 3100*3100 is represented as a 310*310 array.
If image resolutions are sufficently small this may be fixed later.

Currently unsure of what format precisely the Expert annotations will be 
loaded in, so I assume for now they are identical to the MTurk annotations.

"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import pandas as pd
import re

########################
# SCRIPT VARIABLE INPUTS
########################

# row index/URL
# downscale
# show images: worker/expert/intersect/decline
# approval threshold

########################
# SCRIPT VARIABLE INPUTS
########################

# import csv as datatable, then relabel headers
batch_results = pd.read_csv(\
                "batch_results.csv",\
                    usecols=[\
                    'Input.image_url',\
                    'Answer.annotatedResult.boundingBoxes',\
                    'Answer.annotatedResult.inputImageProperties.height',\
                    'Answer.annotatedResult.inputImageProperties.width',\
                    'expertAnswer'])

batch_results.columns=['URL','tr_results','y_res','x_res','ex_results']
batch_results.head()

row_count = len(batch_results.index)-1


index = int(input('Select the row index of batch_results.csv (from 0 to 7):'))
if int(index)<=row_count and int(index)>=0:
    c_image = index
    
elif int(index)>=row_count or int(index)<=0:
    print('Input out of bounds. Image index set to 0')
    c_image=0
else:
    print('Input out of bounds. Image index set to 0')
    c_image=0


print("")
scale_input = int(input('Select integer downscaling factor (suggested 10):'))
if int(index)>0:
    scale_factor = scale_input
    
else:
    print('Input out of bounds. Downscale factor set to 10')
    scale_factor = 10





# current image being processed, 1 and 4 indicates column index in dataframe


worker_assignment_raw = batch_results.iloc[c_image,1]
expert_assignment_raw = batch_results.iloc[c_image,4]




##### -----------------------------
## CONVERSION OF worker_assignment_raw to 2d int array
## Removes all extra characters except pixel integers in string

replace = {'"label":"Stone",': "", "{": "", "}": "", '"height":' : "", '"left":' : "", '"top":' : "", '"width":' : "", '[' : "", ']' : ""}
replace = dict((re.escape(k), v) for k, v in replace.items())
pattern = re.compile("|".join(replace.keys()))
war_str_list = pattern.sub(lambda m: replace[re.escape(m.group(0))], worker_assignment_raw)

# convert comma-delimited string list to list of integers
war_int_list = war_str_list.split(",")
war_int_list = [int(i) for i in war_int_list]

war_int_array = np.asarray(war_int_list)
war_int_array = war_int_array.reshape(len(war_int_array)//4, 4)




##### -----------------------------
## CONVERSION OF expert_assignment_raw to 2d int array
## might be changed at some point once I get real expert annotations
##### -----------------------------


# Remove all extra characters except pixel integers in string
replace = {'"label":"Stone",': "", "{": "", "}": "", '"height":' : "", '"left":' : "", '"top":' : "", '"width":' : "", '[' : "", ']' : ""}
replace = dict((re.escape(k), v) for k, v in replace.items())
pattern = re.compile("|".join(replace.keys()))
ear_str_list = pattern.sub(lambda m: replace[re.escape(m.group(0))], expert_assignment_raw)

# convert comma-delimited string list to list of integers
ear_int_list = ear_str_list.split(",")
ear_int_list = [int(i) for i in ear_int_list]

ear_int_array = np.asarray(ear_int_list)
ear_int_array = ear_int_array.reshape(len(ear_int_array)//4, 4)




# print some details on the job being done currently

print('Currently processing image: ')
print(batch_results.iloc[c_image,0])
print("")
print('Worker annotation integer summary array:')
print(war_int_array)
print("")
print('Expert annotation integer summary array:')
print(ear_int_array)
print("")





# create an array for a given image URL of length x*y resolution
# convert any given row of numbers into a one hot vector 3100*3100 long


#starting at the top left point, get x.res
# load image from corresponding URL to use for processing (?)

x_res = int(batch_results.iloc[c_image,3]/scale_factor)
y_res = int(batch_results.iloc[c_image,2]/scale_factor)

# build numpy array of zeros
tr_array = np.zeros((x_res,y_res), dtype=int)
for n_row in range(0,len(war_int_array)):
    
    h_tr = int(round(war_int_array[n_row,0]/scale_factor))
    l_tr = int(round(war_int_array[n_row,1]/scale_factor))
    t_tr = int(round(war_int_array[n_row,2]/scale_factor))
    w_tr = int(round(war_int_array[n_row,3]/scale_factor))

    # converts bounding box covered pixels to 1's 
    tr_array[t_tr:(t_tr+h_tr),l_tr:(l_tr+w_tr)] = 1
    print("Just finished digitizing row number: " + str(n_row))

# uncomment to visualize worker annotation in csv format. Too lazy to make something in matplotlib.
# np.savetxt("arrayvis_worker.csv", tr_array, delimiter=",")
# print("Created visualization of worker annotation.\
#       See in root folder: 'arrayvis_worker.csv'")

        
# build numpy array of zeros
ex_array = np.zeros((x_res,y_res), dtype=int)
for n_row in range(0,len(ear_int_array)):
    
    h_tr = int(round(ear_int_array[n_row,0]/scale_factor))
    l_tr = int(round(ear_int_array[n_row,1]/scale_factor))
    t_tr = int(round(ear_int_array[n_row,2]/scale_factor))
    w_tr = int(round(ear_int_array[n_row,3]/scale_factor))

    # converts bounding box covered pixels to 1's 
    ex_array[t_tr:(t_tr+h_tr),l_tr:(l_tr+w_tr)] = 1
    print("Just finished digitizing row number: " + str(n_row))

# uncomment to visualize expert annotation in csv format.    
# np.savetxt("arrayvis_expert.csv", ex_array, delimiter=",")
# print("Created visualization of worker annotation.\
#       See in root folder: 'arrayvis_expert.csv'")  
    
    

# Calculate intersection (overlap) over union.

if len(tr_array) == len(ex_array) and len(tr_array[1]) == len(ex_array[1]):
    overlap = tr_array * ex_array
    union   = tr_array + ex_array

    agreement = overlap.sum() / float(union.sum()) * 100
    
    print("")
    print('Intersection over union result:')
    print("% "+str(round(agreement,2)))
    print("")
    
    # fill in the agreement
    f = open('batch_results.csv', 'r', newline = '')
    reader = csv.reader(f)
    mylist = list(reader)
    f.close()
    mylist[(c_image+1)][31] = round(agreement,2)
    
    new_batch_results = open('batch_results.csv', 'w', newline = '')
    csv_writer = csv.writer(new_batch_results)
    csv_writer.writerows(mylist)
    new_batch_results.close()
    
    print("Agreement (IOU and %) written to batch_results.csv")
    
    
    
else:
    print("Ensure image resolutions (and array sizes) are identical.")
    print("")
    
    
    
answer = str(input('Show color visualization of arrays (show "worker"/"expert"/"intersect"/"decline"):')).lower().strip()

if answer == "worker":
        
    fig = plt.figure(figsize=(6, 3.2))

    ax = fig.add_subplot(111)
    ax.set_title('Worker array visualization.')
    plt.imshow(tr_array*9)
    plt.show()
    
elif answer == "expert":  

    fig = plt.figure(figsize=(6, 3.2))

    ax = fig.add_subplot(111)
    ax.set_title('Expert array visualization.')
    plt.imshow(ex_array*4)
    plt.show()
    
elif answer == "intersect":
    
    fig = plt.figure(figsize=(6, 3.2))

    ax = fig.add_subplot(111)
    ax.set_title('Intersection array visualization')
    intersect_array = (tr_array*9) + (ex_array*4)
    plt.imshow(intersect_array)
    
    plt.show()
    print('     yellow = intersect')
    print('     green = worker')
    print('     blue = expert')    

else:
    print('Visualizations declined.')
