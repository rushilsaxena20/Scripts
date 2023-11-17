import sys
import boto3
import json

def upload_to_SM_json(secret, secret_name, description, region, team, replication, replication_list):
    client = boto3.client('secretsmanager', region_name =region)
    if replication.lower() == 'yes':
        replication_regions = [json.dumps(json.loads(replication_list))] # take input in the form of json from front end
        # eg: {
        #     'Region': 'string'
        # },
        response = client.create_secret(
        Name=secret_name,
        Description=description,
        SecretString=json.dumps(json.loads(secret)),
        Tags=[
            {
                'Key': 'Name',
                'Value': secret_name
            },
            {
                'Key': 'Business',
                'Value': team
            },
            {
                'Key': 'Owner',
                'Value': 'SecOps'
            }
        ],
        AddReplicaRegions=replication_regions
        )
        return response
    else:
        response = client.create_secret(
            Name=secret_name,
            Description=description,
            SecretString=json.dumps(json.loads(secret)),
            Tags=[
                {
                    'Key': 'Name',
                    'Value': secret_name
                },
                {
                    'Key': 'Business',
                    'Value': team
                },
                {
                    'Key': 'Owner',
                    'Value': 'SecOps'
                }
            ]
            )
        return response

def upload_to_SM_plaintext(secret, secret_name, description, region, team, replication, replication_list):
    client = boto3.client('secretsmanager', region_name =region)
    if replication.lower() == 'yes':
        replication_regions = [json.dumps(replication_list)] # take input in the form of json from front end
        # eg: {
        #     'Region': 'string',
        # }
        response = client.create_secret(
        Name=secret_name,
        Description=description,
        SecretString=str(secret),
        Tags=[
            {
                'Key': 'Name',
                'Value': secret_name
            },
            {
                'Key': 'Business',
                'Value': team
            },
            {
                'Key': 'Owner',
                'Value': 'SecOps'
            }
        ],
        AddReplicaRegions=replication_regions
        )
        return response
    else:
        response = client.create_secret(
            Name=secret_name,
            Description=description,
            SecretString=str(secret),
            Tags=[
                {
                    'Key': 'Name',
                    'Value': secret_name
                },
                {
                    'Key': 'Business',
                    'Value': team
                },
                {
                    'Key': 'Owner',
                    'Value': 'SecOps'
                }
            ]
            )
        return response

def check_secret(secret_name, region):
    client = boto3.client('secretsmanager', region_name =region)
    try:
        response = client.describe_secret(SecretId=secret_name)
        return f"Error: The secret '{secret_name}' exists in AWS Secrets Manager."
    except client.exceptions.ResourceNotFoundException:
        return f"Creating the secret"


if __name__ == "__main__":
    secret_type = sys.argv[1] # plaintext or json
    secret = sys.argv[2]
    secret_name = sys.argv[3]
    description = sys.argv[4]
    region = sys.argv[5]
    team = sys.argv[6]
    replication = sys.argv[7] # yes or no
    replication_list = sys.argv[8]
    check = check_secret(secret_name, region)
    if "Error" not in check:
        if secret_type.lower() == "json":
            upload_to_SM_json(secret, secret_name, description, region, team, replication, replication_list)
        elif secret_type.lower() == "plaintext":
            upload_to_SM_plaintext(secret, secret_name, description, region, team, replication, replication_list)
        else:
            print("Please provide secret type.")
    else:
        print(check)