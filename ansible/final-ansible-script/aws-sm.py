import boto3
import sys
import json

def create_secret(clientname, key, regionname, service, accountid, dctype, envtype):
    print('creating secret')
    """
    This function takes clientname, public key, private key and stores them as a secret in AWS
    secrets manager with appropriate naming.
    """
    # print(public_key)
    if ('private' in key.lower()):
        print('inside if')
        secret_value = {"PrivateKey": key}
        keytype = 'Private'
    else:
        print('inside else')
        secret_value = {"PublicKey": key}
        keytype = 'Public'
    print('xyz')
    try:
        client = boto3.client('secretsmanager', region_name = regionname)
        response = client.create_secret(
            Name=accountid+"_"+dctype+"_"+envtype+"_"+service+"_"+keytype,
            Description="This is a secret for tenant " + clientname,
            SecretString=json.dumps(secret_value),
            Tags=[
                {
                    'Key': 'Name',
                    'Value': clientname
                },
                {
                    'Key': 'Business',
                    'Value': "security"
                },
                {
                    'Key': 'Owner',
                    'Value': 'SecOps'
                },
                { 
                    'Key': 'Service',
                    'Value': service
                }
            ]
        )
        print(response)
        return response
    except Exception as e:
        print(e)
        return e
def readfile(filepath):
    with open(filepath, 'r') as f:
        file = f.read()
        # print(file)
    return file.strip('\n')
def main(clientname, public_key, private_key, regionname, service, accountid, dctype, envtype):
    public_key = readfile(public_key)
    private_key = readfile(private_key)
    create_secret(clientname, public_key, regionname, service, accountid, dctype, envtype)
    create_secret(clientname, private_key, regionname, service, accountid, dctype, envtype)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8])



