from botocore.exceptions import ClientError
import dotenv
import boto3
import os

dotenv.load_dotenv()

# S3 연결 준비
client_s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("CREDENTIALS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("CREDENTIALS_SECRET_KEY")
)


def upload_file(filename):
    filename = str(filename)
    try:
        if not isinstance(filename, str):
            raise TypeError("Filename must be a string")
        print(filename)
        client_s3.upload_file(
            f"./images/{filename}",
            os.getenv("S3_BUCKET"),
            f"images/{filename}",
            ExtraArgs={'ContentType': 'image/webp'}
        )

    except ClientError as e :
        print(f'Credential error => {e}')
    except TypeError as e:
        print(f'Type error => {e}')
    except Exception as e :
        print(f"Another error => {e}")
