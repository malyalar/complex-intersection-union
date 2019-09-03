# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 10:13:13 2019
@author: Rohit

This script does three things:
    1) builds a dataframe of unique worker ID's who have completed assignments.
    2) calculates the average intersection/union score for each worker
       (only applicable to assignments that HAVE an expert's annotation.)
    3) outputs a acceptance/rejection to these workers.

"""

import re
import pandas as pd
import math
import csv


csv_filename = 'batch_results.csv'

start_df = pd.read_csv(csv_filename, usecols=['WorkerId', 'IOUrating'])
new_df = start_df.groupby('WorkerId').mean()
new_df = new_df.reset_index()
new_df = new_df.assign(approve="")



# create reference dataframe

for index in range(0,len(new_df)):

    worker_id = new_df.iloc[index,0]
    worker_score = new_df.iloc[index,1]

    if worker_score >= 50:
        new_df.iloc[index,2] = 1
    elif math.isnan(worker_score):
        new_df.iloc[index,2] = None
    else:
        new_df.iloc[index,2] = 0



# use reference dataframe to edit batch_results.csv

for index in range(0,len(new_df)):

    worker_id = new_df.iloc[index,0]
    worker_approve = bool(new_df.iloc[index,2])

    f = open(csv_filename, 'r', newline = '')
    reader = csv.reader(f)
    mylist = list(reader)

    for index2 in range(1,len(mylist)):
        if mylist[(index2)][15] == worker_id and new_df.iloc[index,2] != None:
            mylist[(index2)][31] = worker_approve
            mylist[(index2)][32] = not worker_approve
        elif new_df.iloc[index,2] == None:
            mylist[(index2)][31] = "None"
            mylist[(index2)][32] = "None"
        else:
            pass

    f.close()

    new_batch_results = open(csv_filename, 'w', newline = '')
    csv_writer = csv.writer(new_batch_results)
    csv_writer.writerows(mylist)
    new_batch_results.close()
