import boto3
import sys
from botocore.exceptions import ClientError
import requests

iam = boto3.client('iam')

def upload_Secret_To_Vault(token, username, access_key, secret_key, account):
    headers = {
    'Content-Type': 'application/json',
    'X-Vault-Token': token
    }
    json_data = {
        'data': {
            'AccessKey': access_key,
            'SecretKey': secret_key,
            'Account': account
        },
    }
    # response = requests.get('https://vault-prod.moengage.com/v1/security/data/api_testing', headers=headers)
    response = requests.post(f'https://vault-prod.moengage.com/v1/AWS_Users/data/{username}-{account}', headers=headers, json=json_data)
    if response.status_code == 200:
        print("Stored Access and Secret keys in the HashiCorp Vault.")
    else:
        print("There were some errors in storing the secrets in HashiCorp Vault, please connect with SecOps team.")

def create_user(username, owner):
    try:
        response = iam.create_user(
            UserName=username
        )
        print(f'Created IAM user {username}')
        
        access_key_response = iam.create_access_key(
            UserName=username
        )
        access_key_id = access_key_response['AccessKey']['AccessKeyId']
        secret_access_key = access_key_response['AccessKey']['SecretAccessKey']
        print(f'Created access key for IAM user {username}')
        # print(f'Access key ID: {access_key_id}')
        # print(f'Secret access key: {secret_access_key}')
        tags = [
        {
            'Key': 'Name',
            'Value': f'{username}'
        },
        {
            'Key': 'Owner',
            'Value': f'{owner}'
        },
        {
            'Key': 'Created_By',
            'Value': f'Harness_Pipeline'
        }
        ]   
        iam.tag_user(
            UserName=username,
            Tags=tags
        )
        return [access_key_id, secret_access_key]
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            return f'Error: IAM user {username} already exists'
        else:
            return f'Error: creating IAM user {username}: {e}'

if __name__ == "__main__":
    username = sys.argv[1]
    owner = sys.argv[2]
    token = sys.argv[3]
    account = sys.argv[4]
    response = create_user(username, owner)
    if 'Error' not in response:
        upload_Secret_To_Vault(token, username, response[0], response[1], account)
    else:
        print(response)
