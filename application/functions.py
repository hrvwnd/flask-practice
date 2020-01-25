import boto3
import botocore
import logging
from botocore.exceptions import ClientError
import requests

def save_photo(f):
    filename = secure_filename(f.filename)
    try:
        f.save(os.path.join(
            app.instance_path, '/tmp/photos', filename
        ))
    except Exception as e:
        print ("File error")
        return False
    return True


def s3upload_file(file):
    BUCKET_NAME = "automate-static-1579254877"
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(('/tmp/photos/' + file, BUCKET_NAME, file )
    except ClientError as e:
        logging.error(e)
        return False
    return True    


def create_url(object_name, bucket_name):
    expiration = 3600
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
            Params={
                'Bucket': bucket_name,
                'Key': object_name},
                ExpiresIn=expiration
                    )
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response


def download_url(url):
    if url is not None:
        response = requests.get(url)
        with open("/home/ubuntu/tmp/photos","wb") as photodir:
            photodir.write(response.content)


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
