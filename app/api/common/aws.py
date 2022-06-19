import boto3
import os
from botocore.exceptions import ClientError


# * Save File In AWS S3
def upload_to_s3(file_name, bucket, object_name):

    upload = upload_file_new(file_name, bucket, object_name)
    if upload is True:
        link = create_presigned_url(bucket, object_name)
        if link is None:
            print("Link generation to uploaded image: Failed")
            return {
                "message": "Internal server Error",
                "status_code": 500
            }
        else:
            return {
                "message": "Link generated successfully.",
                "link": link,
                "status_code": 200
            }
    else:
        print("Uploading Image to AWS S3 : Failed")
        return {
            "message": "Internal server Error.",
            "status_code": 500
        }


def create_presigned_url(bucket_name, object_name, expiration=3600):
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration,
                                                    HttpMethod='GET'
                                                    )
    except ClientError as e:
        return None
    return response


def generate_presign_link(bucket_name, object_name):
    client = boto3.client('s3')
    res = client.generate_presigned_url(
        'get_object', Params={'Bucket': bucket_name, 'Key': object_name}, ExpiresIn=3600)
    if res:
        return{
            'text': 'exist',
            'link': res,
            'status_code': 200
        }
    else:
        return {
            'text': 'Not Exists',
            'link': "",
            'status_code': 500
        }


def upload_file_new(file_name, bucket, object_name):
    # Creating Session With Boto3.
    try:
        session = boto3.Session(
            aws_access_key_id=os.environ.get('AWS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_KEY')
        )

        # Creating S3 Resource From the Session.
        s3 = session.resource('s3')
        print(file_name)
        result = s3.Bucket(bucket).upload_file(file_name, object_name)

        print(result)
        return True
    except Exception as e:
        print(e)
        return False
