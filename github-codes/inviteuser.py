import requests
import json
import sys
import boto3
import get_secret

def inviteuser(org_name, email, secret):
    headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {secret}',
        'X-GitHub-Api-Version': '2022-11-28',
    }
    data = {"email":"","role":"direct_member","team_ids":[]}
    data['email'] = email
    response = requests.post(f'https://api.github.com/orgs/{org_name}/invitations', headers=headers, data=json.dumps(data))
    if response.status_code == 201:
        print('GitHub invitation sent, please check and make sure 2FA is enabled. NOTE: If 2FA is not enabled, access will be revoked.')
    elif response.status_code==422:
        for error in response.json()['errors']:
            if 'A user with this email addresss is already a part of this org' in error['message']:
                print('A user with this email addresss is already a part of this organization')
            else:
                print('Please connect with SecOps team')
    else:
        print('Please connect with SecOps team')

if __name__ == '__main__':
    # print(sys.argv[1])
    secret = get_secret.get_secret('rushil_gh_token')
    # print(secret)
    inviteuser('MoEngage',sys.argv[1], secret)