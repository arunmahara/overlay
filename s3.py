import boto3
from botocore.config import Config


def get_s3_client(config):
    return boto3.client(
        's3',
        aws_access_key_id=config['S3_ACCESS_KEY'],
        aws_secret_access_key=config['S3_ACCESS_SECRET'],
        config=Config(
            signature_version='s3v4',
            region_name=config['S3_REGION']
        )
    )


def upload_file_to_s3(local_file_path: str, document_name: str, config: str):
    try:
        bucket_name = config['S3_BUCKET']
        s3_document_folder = config['S3_DOCUMENT_FOLDER']
        s3_key = f"{s3_document_folder}/{document_name}"

        s3_client = get_s3_client(config)
        s3_client.upload_file(local_file_path, bucket_name, s3_key, ExtraArgs={'ContentType': "image/jpeg"})

        return s3_key
    except Exception as e:
        raise e


def get_signed_url(s3_key: str, config: str):
    try:
        bucket_name = config['S3_BUCKET']
        ttl = config['DOC_LINK_EXPIRY_SECS']

        s3_client = get_s3_client(config)
        response = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': s3_key
            },
            ExpiresIn=ttl
        )

        return response
    except Exception as e:
        raise e
