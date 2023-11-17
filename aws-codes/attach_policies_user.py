import sys
import boto3
from botocore.exceptions import ClientError

def attachPolicyToUser(user_name, policy_arns):
    # create IAM client
    iam = boto3.client('iam',region_name="us-east-1")

    # attach policies to user
    for policy_arn in policy_arns:
        try:
            response = iam.attach_user_policy(
                PolicyArn=policy_arn,
                UserName=user_name
            )
            print("Successfully attached policy {} to user".format(policy_arn))
        except ClientError as e:
            print("Error attaching policy {} to user: {}".format(policy_arn, e))


def getArnFromName(policies, account):
    if account == 'Prod':
        account_id = "612427630422"
    elif account == 'DC05':
        account_id = "163129101105"
    else:
        print("account not defined")
    policies_arn = []
    correct_policies = []
    # create IAM client
    iam = boto3.client('iam', region_name="us-east-1")
    templatepolicyarn = {"CustomerManaged": f"arn:aws:iam::{account_id}:policy/", 
                        "AWSManaged": "arn:aws:iam::aws:policy/", 
                        "AWSManagedJobFunction": "arn:aws:iam::aws:policy/job-function/"} 

    for policy_name in policies:
        for policytype in templatepolicyarn.keys():
            try:
                response = iam.get_policy( PolicyArn=f'{templatepolicyarn[policytype]}{policy_name}')
                policy_arn = response['Policy']['Arn']
                policies_arn.append(policy_arn)
                correct_policies.append(policy_name)
            except ClientError as e:
                if e.response['Error']['Code'] == 'NoSuchEntity':
                    pass
                else:
                    print("Error getting policy ARN for {}: {}".format(policy_name, e))
                    break
    
    wrong_policies = set(policies) - set(correct_policies)
    if len(wrong_policies) != 0:
        print(f"Error getting policy ARN for {wrong_policies}")
    return policies_arn

def main(user_name, policies, account):
    policies = policies.replace(" ", "").split(",")
    # policies = [BillingFull, Billing, CloudFrontFullAccess, Biling, "CloudFrontFullAcces"]
    arnres = getArnFromName(policies, account)
    attachPolicyToUser(user_name, arnres)


if __name__ == "__main__":
    user_name= sys.argv[1]
    policies= sys.argv[2]
    account= sys.argv[3]
    main(user_name, policies, account)
