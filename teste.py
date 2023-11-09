import argparse
import boto3
import json
import sys
from colorama import init, Fore

init(strip=False)
print(r"""{}
                                                                                                                                                                       

                ░░░░█▐▄▒▒▒▌▌▒▒▌░▌▒▐▐▐▒▒▐▒▒▌▒▀▄▀▄░
                ░░░█▐▒▒▀▀▌░▀▀▀░░▀▀▀░░▀▀▄▌▌▐▒▒▒▌▐░
                ░░▐▒▒▀▀▄▐░▀▀▄▄░░░░░░░░░░░▐▒▌▒▒▐░▌
                ░░▐▒▌▒▒▒▌░▄▄▄▄█▄░░░░░░░▄▄▄▐▐▄▄▀░░
                ░░▌▐▒▒▒▐░░░░░░░░░░░░░▀█▄░░░░▌▌░░░
                ▄▀▒▒▌▒▒▐░░░░░░░▄░░▄░░░░░▀▀░░▌▌░░░
                ▄▄▀▒▐▒▒▐░░░░░░░▐▀▀▀▄▄▀░░░░░░▌▌░░░
                ░░░░█▌▒▒▌░░░░░▐▒▒▒▒▒▌░░░░░░▐▐▒▀▀▄
                ░░▄▀▒▒▒▒▐░░░░░▐▒▒▒▒▐░░░░░▄█▄▒▐▒▒▒
                ▄▀▒▒▒▒▒▄██▀▄▄░░▀▄▄▀░░▄▄▀█▄░█▀▒▒▒▒
                                               
                                                                                                                                                        
                    {}{}☁️{}   CSIRT Cloud Automation 
                                        
    """.format(Fore.LIGHTBLACK_EX, Fore.BLUE,
               Fore.LIGHTBLACK_EX, Fore.WHITE))


parser = argparse.ArgumentParser(description="",
    usage='use "%(prog)s --help" for more information',
    formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('command', help='Command to execute', choices=['list-s3', 'list-objects', 'get-tags-s3', 'list-ec2', 'get-tags-ec2', 'list-roles', 'list-eks', 'list-cloudfront', 'list-route53'])
parser.add_argument('--bucket', help='Name of the S3 bucket to list objects in or get tags from', required=False)
parser.add_argument('--instance-id', help='ID of the EC2 instance to get tags from', required=False)


args = parser.parse_args()



################################## BUCKET S3 ##################################

if args.command == 'list-s3':
    s3 = boto3.client('s3')
    response = s3.list_buckets()

    print("S3 Buckets:")
    for bucket in response['Buckets']:
        print(f"- {bucket['Name']}")

elif args.command == 'list-objects':
    if not args.bucket:
        print("Error: You must provide the --bucket argument for 'list-objects' command.")
    else:
        s3 = boto3.client('s3')
        response = s3.list_objects_v2(Bucket=args.bucket)

        print(f"S3 Objects in '{args.bucket}':")
        for obj in response.get('Contents', []):
            print(f"- {obj['Key']}")

elif args.command == 'get-tags-s3':
    if not args.bucket:
        print("Error: You must provide the --bucket argument for 'get-tags-s3' command.")
    else:
        s3 = boto3.client('s3')
        
        # Obtém as tags do bucket especificado
        try:
            response = s3.get_bucket_tagging(Bucket=args.bucket)
            tags = response['TagSet']
            
            print(f"Tags for bucket '{args.bucket}':")
            for tag in tags:
                print(f"- {tag['Key']}: {tag['Value']}")
        except Exception as e:
            print(f"Error: {e}")

################################## EC2 ##################################

elif args.command == 'list-ec2':
    ec2 = boto3.client('ec2', region_name='sa-east-1')

    # Lista as instâncias EC2
    response = ec2.describe_instances()

    print("EC2 Instances:")
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(f"Instance ID: {instance['InstanceId']}")
            print(f"Instance Type: {instance['InstanceType']}")
            print(f"State: {instance['State']['Name']}")
            for interface in instance['NetworkInterfaces']:
                print(f"Private IP: {interface['PrivateIpAddress']}")
                print(f"Public IP: {interface.get('Association', {}).get('PublicIp', 'N/A')}")
                print(f"Elastic IP: {interface.get('Association', {}).get('PublicIp', 'N/A')}")
            print(f"Launch Date: {instance['LaunchTime']}")
            print()

elif args.command == 'get-tags-ec2':
    if not args.instance_id:
        print("Error: You must provide the --instance-id argument for 'get-tags-ec2' command.")
    else:
        ec2 = boto3.client('ec2', region_name='sa-east-1')

        # Obtém as tags da instância EC2 especificada
        try:
            response = ec2.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [args.instance_id]}])

            print(f"Tags for EC2 Instance ID '{args.instance_id}':")
            for tag in response['Tags']:
                print(f"- {tag['Key']}: {tag['Value']}")
        except Exception as e:
            print(f"Error: {e}")

################################## IAM ROLES ##################################

elif args.command == 'list-roles':
    iam = boto3.client('iam')
    response = iam.list_roles()
    
    print("IAM Roles:")
    for role in response['Roles']:
        role_name = role['RoleName']
        create_date = role['CreateDate']
        print(f"RoleName: {role_name}\nCreateDate: {create_date}")
        print('=' * 40)


################################## OTHERS ##################################

# Listar Amazon EKS Clusters
elif args.command == 'list-eks':
    eks = boto3.client('eks')
    response = eks.list_clusters()

    print("Amazon EKS Clusters:")
    for cluster in response['clusters']:
        print(f"- {cluster}")

# Listar distribuições CloudFront
elif args.command == 'list-cloudfront':
    cloudfront = boto3.client('cloudfront')
    response = cloudfront.list_distributions()

    print("CloudFront Distributions:")
    for distribution in response['DistributionList']['Items']:
        print(f"- {distribution['Id']}")

# Listar zonas hospedadas Route 53
elif args.command == 'list-route53':
    route53 = boto3.client('route53')
    response = route53.list_hosted_zones()

    print("Route 53 Hosted Zones:")
    for hosted_zone in response['HostedZones']:
        print(f"- {hosted_zone['Name']}")



      
