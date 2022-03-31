#script by rikardoroa
#Just python it!
import boto3
from Azure_blobs_download import *
from dotenv import load_dotenv

load_dotenv()


class AWSBucket:
    # secret keys
    AWS_secret = os.getenv('AWS_Secret')
    AWS_key = os.getenv('AWS_Key_ID')
    AWS_region = os.getenv('AWS_Region')
    Bucket = os.getenv('Bucket')
    Principal = os.getenv('Principal')
    Resource = os.getenv('Resource')

    # var initialization
    def __init__(self, secret=AWS_secret, key=AWS_key, region=AWS_region, session=boto3.Session, principal=Principal,
                 resource=Resource, awsbucket=Bucket, data=list):
        self.secret = secret
        self.region = region
        self.key = key
        self.session = session
        self.bucket = awsbucket
        self.principal = principal
        self.resource = resource
        self.data = data

    def bucket_creation(self):
        # initializing session
        session = boto3.Session(aws_access_key_id=self.key, aws_secret_access_key=self.secret, region_name=self.region)
        # creating a bucket in aws services
        s3 = session.client('s3')
        s3n = session.resource('s3', region_name=self.region)
        try:
            s3.create_bucket(Bucket=self.bucket, CreateBucketConfiguration={'LocationConstraint': self.region})
        except s3n.meta.client.exceptions.BucketAlreadyOwnedByYou:
            s3n.Bucket(name=self.bucket)
            print('Bucket already exist')
        self.session = session


    def bucket_policy(self):
        # init vars
        session = self.session
        s3 = session.client("s3")
        # defining bucket policy
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "Statement1",
                    "Principal": {"AWS": self.principal},
                    "Effect": "Allow",
                    "Action": "*",
                    "Resource": [self.resource]
                }
            ]
        }
        # applying policy
        policy_string = json.dumps(bucket_policy)
        policy = s3.put_bucket_policy(Bucket=self.bucket, Policy=policy_string)
        # public access restriction policy
        response_public = s3.put_public_access_block(
            Bucket=self.bucket,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            },
        )
        print('Applying Bucket Policy')
        return policy, response_public



    def run_bucket_creation_policy(self):
        # Running all functions in the main module
        thread_one = threading.Thread(target=self.bucket_creation)
        thread_one.start()
        thread_one.join()
        thread_two = threading.Thread(target=self.bucket_policy)
        thread_two.start()
        thread_two.join()
        return thread_one, thread_two


