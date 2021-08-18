import boto3
import boto3.session
from botocore.client import Config
import os
import urllib3

region2 = os.environ.get('REGION')
print(region2)
#REGION=$(curl http://169.254.169.254/latest/meta-data/placement/region)
#session = boto3.session.Session()
#region = session.region_name
#region = 'us-east-2'
client= boto3.client('s3')
region = client.meta.region_name
print(region)

print("running 3")
http = urllib3.PoolManager()
r = http.request('GET', 'http://169.254.169.254/latest/meta-data/placement/region')
#response = urllib.request.urlopen('https://169.254.169.254/latest/meta-data/placement/region')
print(r.status)
region3 = r.data
region3 = region3.decode("utf-8")
print(region3)


def upload_file(file_name, bucket):
    object_name = file_name
    s3_client = boto3.client('s3',endpoint_url=f'https://s3.{region3}.amazonaws.com',config=Config(signature_version='s3v4',s3={'addressing_style': 'path'}))
    response = s3_client.upload_file(file_name, bucket, object_name)
    return response

def list_files(bucket):                                                                             
    s3_client = boto3.client('s3',endpoint_url=f'https://s3.{region3}.amazonaws.com',config=Config(signature_version='s3v4',s3={'addressing_style': 'path'}))
    contents = []
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            # print(item)
            contents.append(item)
    except Exception as e:
        pass
    return contents
                                                                                                    
def show_image(bucket):
    s3_client = boto3.client('s3',endpoint_url=f'https://s3.{region3}.amazonaws.com',config=Config(signature_version='s3v4',s3={'addressing_style': 'path'}))
    # location = boto3.client('s3').get_bucket_location(Bucket=bucket)['LocationConstraint']
    public_urls = []
    try:
        for item in s3_client.list_objects(Bucket=bucket)['Contents']:
            presigned_url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': item['Key']}, ExpiresIn = 100)
            # print("[DATA] : presigned url = ", presigned_url)
            public_urls.append(presigned_url)
    except Exception as e:
        pass
    # print("[DATA] : The contents inside show_image = ", public_urls)
    return public_urls