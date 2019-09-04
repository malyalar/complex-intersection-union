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

session = boto3.session.Session(region_name=region)
s3client = session.client('s3', config= boto3.session.Config(signature_version='s3v4'))


# List all the buckets with the account
bucket_list = s3.list_buckets()
print('Existing Buckets: ')

for bucket in bucket_list['Buckets']:
    print(f' {bucket["Name"]}')


# list objects
object_list = s3.list_objects(Bucket='lithotripsystonefinder')


with open('input.csv', 'w', newline='') as csvFile:

    writer = csv.writer(csvFile)

    for key in object_list['Contents']:
    
        # s3client.get_object(Bucket='lithotripsystonefinder', Key=key['Key'])
        presigned_url = s3client.generate_presigned_url('get_object',
        Params={
          'Bucket': "lithotripsystonefinder",
          'Key': key['Key'],
          },
        ExpiresIn=604800,
        )
        writer.writerow([presigned_url])


# replace the header [0] slot with "input_url"

f = open('input.csv', 'r', newline = '')
reader = csv.reader(f)
mylist = list(reader)
f.close()
mylist[0] = ['image_url']

my_new_list = open('input.csv', 'w', newline = '')
csv_writer = csv.writer(my_new_list)
csv_writer.writerows(mylist)
my_new_list.close()
