# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 16:24:00 2019

@author: Rohit Malyala
"""

import boto3
import csv

"""
The contents of this comment section should ideally be hidden away in a 
credentials file. They are kept open here for the sake of pointing out
how another user might put use their own accounts for the purpose.
Uncomment this file to run the python script on any computer.

region = 'us-east-1'
aws_access_key_id = 'XXXXXXXXXXXXXXXXXX'
aws_secret_access_key = 'XXXXXXXXXXXXXXXXXXXXX+XXXX'
"""

# create client object    
client = boto3.client(
    's3',
    region_name=region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key
    )

# Interesting conda CLI argument: aws s3 ls s3://<name_of_bucket>/<key_prefix>/ --recursive

# List all the buckets with the account
bucket_list = client.list_buckets()
print('Existing Buckets: ')

for bucket in bucket_list['Buckets']:
    print(f' {bucket["Name"]}')

# create a raw list of the objects or contents of the bucket.
object_list = client.list_objects(Bucket='lithotripsystonefinder')

# get URL for the bucket of interest
URL_header ='https://lithotripsystonefinder.s3.ca-central-1.amazonaws.com/'

# parsing function to get 'key' just makes a list of only
for key in object_list['Contents']:
    print(URL_header + key['Key'])


# arrange unordered dictionary into an array


# create CSV with URLs 
# 'image_url' is the name of the header
    
with open('input.csv', 'w', newline='') as csvFile:
    writer = csv.writer(csvFile)
   
    for key in object_list['Contents']:
        URL_full = URL_header + key['Key']
        writer.writerow([URL_full])


f = open('input.csv', 'r', newline = '')
reader = csv.reader(f)
mylist = list(reader)
f.close()
mylist[0] = ['input_url']

my_new_list = open('input.csv', 'w', newline = '')
csv_writer = csv.writer(my_new_list)
csv_writer.writerows(mylist)
my_new_list.close()































