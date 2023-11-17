import gnupg
import sys
import boto3
import json

def generate_gpg_keys(name, passphrase):
    
    input_data = gpg.gen_key_input(
        key_type = "RSA",
        key_length=4096,
        name_real = name,
        name_email = 'secops@moengage.com',
        passphrase = passphrase   
    )
    key = gpg.gen_key(input_data)
    # print(key)
    keys = gpg.list_keys()
    keyid = ''
    uid = ''
    for id in keys:
        if id['fingerprint'] == key.fingerprint:
            print(id['keyid'])
            keyid = id['keyid']
            print(id['uids'])
            uid = id['uids']
    return key.fingerprint, keyid, uid

def upload_to_SM(public_key, private_key, keyid, uid, name, passphrase, db_name, region):
    client = boto3.client('secretsmanager', region_name =region)
    secret_value = {
            "PublicKey" : public_key,
            "PrivateKey" : private_key,
            "Passphrase" : passphrase,
            "Keyid" : keyid,
            "uid" : str(uid)
            }
    response = client.create_secret(
        Name=f"pgp_keys_{db_name}",
        Description=f"This is a secret for tenant {name}",
        SecretString=json.dumps(secret_value),
        Tags=[
            {
                'Key': 'Name',
                'Value': name
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
                'Value': 'PGP'
            }
        ]
        )
    return response   

def check_secret(db_name, region):
    client = boto3.client('secretsmanager', region_name=region)
    try:
        response = client.describe_secret(
            SecretId=f"pgp_keys_{db_name}"
            )   
        return False
    except Exception as e:
        return True

if __name__ == '__main__':
    gpg = gnupg.GPG()
    check = check_secret(sys.argv[3], sys.argv[4])
    finalop = []
    if check:
        fingerprint, keyid, uid = generate_gpg_keys(sys.argv[1], sys.argv[2])
        public_key = gpg.export_keys(fingerprint)
        private_key = gpg.export_keys(fingerprint, secret=True, passphrase=sys.argv[2])
        sm_value = upload_to_SM(public_key, private_key, keyid, uid, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        print(public_key)
        print(keyid)
        print(uid)
        finalop.append(public_key)
        finalop.append(keyid)
        finalop.append(uid)
    else:
        print("Please check with secops team, there seems to be some issue.")