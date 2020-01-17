import boto3
import botocore

def s3upload_file(file):
    BUCKET_NAME = "automate-static-1579254877"
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file('/tmp/photos/'+file, BUCKET_NAME, file )

def s3download_file(file):
    BUCKET_NAME = "automate-static-1579254877"
    KEY = boto3.resource('s3')
    try:
         s3.Bucket(BUCKET_NAME).download_file(KEY, file)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print ("Object does not exist")
        else:
            raise

def download_file(file):
    pass
