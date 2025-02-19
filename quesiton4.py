import boto3
import csv

def check_iam_roles_for_admin_access(iam_client):
    """Check IAM roles for overly permissive policies like AdministratorAccess."""
    roles = iam_client.list_roles()['Roles']
    results = []

    for role in roles:
        role_name = role['RoleName']
        policies = iam_client.list_attached_role_policies(RoleName=role_name)['AttachedPolicies']
        
        for policy in policies:
            if policy['PolicyName'] == 'AdministratorAccess':
                results.append([role_name, policy['PolicyName']])

    write_to_csv('iam_roles_overly_permissive.csv', ['IAMRoleName', 'PolicyName'], results)

def check_mfa_status_for_users(iam_client):
    """Verify MFA is enabled for all IAM users."""
    users = iam_client.list_users()['Users']
    results = []

    for user in users:
        user_name = user['UserName']
        mfa_devices = iam_client.list_mfa_devices(UserName=user_name)['MFADevices']
        mfa_enabled = 'True' if mfa_devices else 'False'
        results.append([user_name, mfa_enabled])

    write_to_csv('iam_users_mfa_status.csv', ['IAMUserName', 'MFAEnabled'], results)

def check_security_groups_for_public_access(ec2_client):
    
    security_groups = ec2_client.describe_security_groups()['SecurityGroups']
    results = []

    for sg in security_groups:
        sg_name = sg['GroupName']
        for permission in sg['IpPermissions']:
            if 'FromPort' in permission and permission['FromPort'] in [22, 80, 443]:
                for ip_range in permission.get('IpRanges', []):
                    if ip_range['CidrIp'] == '0.0.0.0/0':
                        results.append([sg_name, permission['FromPort'], ip_range['CidrIp']])

    write_to_csv('security_groups_public_access.csv', ['SGName', 'Port', 'AllowedIP'], results)

def check_unused_ec2_key_pairs(ec2_client):
    """Identify unused EC2 key pairs."""
    key_pairs = ec2_client.describe_key_pairs()['KeyPairs']
    instances = ec2_client.describe_instances(Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])['Reservations']
    used_keys = {instance['KeyName'] for reservation in instances for instance in reservation['Instances'] if 'KeyName' in instance}
    results = [[key_pair['KeyName']] for key_pair in key_pairs if key_pair['KeyName'] not in used_keys]

    write_to_csv('unused_ec2_key_pairs.csv', ['KeyName'], results)

def write_to_csv(filename, headers, data):
   
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

def main():
   
    iam_client = boto3.client('iam')
    ec2_client = boto3.client('ec2')

  
    check_iam_roles_for_admin_access(iam_client)
    check_mfa_status_for_users(iam_client)
    check_security_groups_for_public_access(ec2_client)
    check_unused_ec2_key_pairs(ec2_client)

if __name__ == "__main__":
    main()
