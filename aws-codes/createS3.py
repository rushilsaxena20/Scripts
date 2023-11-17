import boto3
import json
import sys
from botocore import exceptions

def create_s3_bucket(bucket_name, region, versioning, team_name, owner):
    s3_client = boto3.client('s3')
    try:
        bucket_Check = s3_client.head_bucket(Bucket=bucket_name)
        if bucket_Check['ResponseMetadata']['HTTPStatusCode'] == 200:
            return(f'Bucket {bucket_name} already exists')
    except exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            try:
                if region == 'us-east-1':
                    response = s3_client.create_bucket(
                        Bucket=bucket_name,
                        ObjectLockEnabledForBucket=False
                    )
                else:
                    response = s3_client.create_bucket(
                        Bucket=bucket_name,
                        CreateBucketConfiguration={
                            'LocationConstraint': region
                        },
                        ObjectLockEnabledForBucket=False
                    )
                tags = [
                    {
                        'Key': 'Name', 
                        'Value': f'{bucket_name}'
                    },
                    {
                        'Key': 'Business', 
                        'Value': f'{team_name}'
                    },
                    {
                        'Key': 'Owner', 
                        'Value': f'{owner}'
                    }
                    ]
                bucket_tags = s3_client.put_bucket_tagging(
                    Bucket=bucket_name,
                    Tagging={'TagSet': tags}
                    )
                if versioning == 'yes':
                    s3_client.put_bucket_versioning(
                        Bucket=bucket_name,
                        VersioningConfiguration={
                            'Status': 'Enabled'
                        }
                    )
                    return(f"Bucket {bucket_name} created successfully in the {region} region, with versioning enabled.")
                else:
                    return(f"Bucket {bucket_name} created successfully in the {region} region.")
            except exceptions.ParamValidationError:
                return(f"Invalid bucket name, bucket names should be unique and should consist of lowercase letters, numbers, periods and hyphens.")
            except exceptions.ClientError as e:
                return(f"An error occured while creating the bucket: {e}, please connect with SecOps team.")
        elif e.response['Error']['Code'] == '403':
            return('Bucket name must be unique within the global namespace and follow the bucket naming rules.')
        else:
            return(f"En error occured, please connect with SecOps team.")
    except Exception as e:
        return(e)

if __name__ == "__main__":
    result = create_s3_bucket(sys.argv[1],sys.argv[2],sys.argv[3], sys.argv[4], sys.argv[5])
    print(result)