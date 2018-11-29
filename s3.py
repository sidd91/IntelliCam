import boto3
import botocore
import numpy as np
#import pandas as pd


Bucket_Name = 'intellicamframes'
KEY = 'data.jpg'

s3 = boto3.resource('s3')

try:
	s3.Bucket(Bucket_Name).upload_file(KEY, "/home/siddharth/work/IntelliCam/data.jpg" )
except botocore.exceptions.ClientError as e:
	if e.response['Error']['Code'] == "404":
		print("The object does not exist")
	else: 
		raise
