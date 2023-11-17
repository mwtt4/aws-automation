import argparse
import boto3
import json
import sys
import os
from colorama import init, Fore
from datetime import datetime



 
class CustomFormatter(argparse.HelpFormatter):
    def _format_action(self, action):
        if action.nargs == 0:
            # Adicione um espaçamento maior entre as opções e descrições
            return super()._format_action(action) + '\n\n'
        return super()._format_action(action)
    

parser = argparse.ArgumentParser(description="AWS CSIRT AUTOMATION",
    usage='use "%(prog)s --help" for more information',
    formatter_class=argparse.RawTextHelpFormatter)


    
init(strip=False)
print(r"""{}
 
                                                                                                                                                                       
                    ⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⠿⢿⣶⡄⠀⠀⠀⠀⠀⢀⣴⣾⠿⢿⣶⣄⠀⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⠀⣰⣿⠏⠀⠀⠀⠻⣿⣆⠀⠀⠀⢠⣿⡟⠁⠀⠀⠙⣿⣧⠀⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⠀⣰⣿⠋⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⡏⠀⠀⠀⠀⠀⠈⢿⣧⠀⠀⠀⠀⠀
                    ⠀⠀⠀⠀⣰⣿⠇⠀⠀⠀⠀⠀⠀⠀⢧⠿⣧⠿⣴⠀⠀⠀⠀⠀⠀⠀⠘⣿⣧⠀⠀⠀⠀
                    ⢰⣿⣿⣿⣿⣧⣤⠀⠀⠀⢀⣀⠀⠀⠀⠀⣤⡀⠀⠀⠀⣀⡀⠀⠀⠀⣤⣼⣿⣿⣿⣿⡆
                    ⢀⣤⣿⣿⣯⣭⣭⠀⠀⠀⢿⣿⡇⠀⢀⣤⣿⣧⡄⠀⢸⣿⣿⠀⠀⠀⣭⣭⣽⣿⣯⣤⡀
                    ⠘⢻⣿⠏⠉⠉⠉⠀⠀⠀⠈⠉⠀⠀⠀⠉⠉⠉⠁⠀⠀⠉⠁⠀⠀⠀⠉⠉⠉⠙⣿⣿⠃
                    ⢀⣿⣟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣹⣿⡄ 
                                                                
                                                                                                                                                        
                    {}{}☁️{}   CSIRT Cloud Automation 
                                        
    """.format(Fore.LIGHTBLACK_EX, Fore.BLUE,
               Fore.LIGHTBLACK_EX, Fore.WHITE))


    
parser.add_argument('command', help='Command to execute', choices=['list-s3', 'list-objects', 'get-tags-s3', 'list-ec2', 'get-tags-ec2', 'list-roles', 'list-eks', 'list-cloudfront', 'list-route53','priv-s3','info','list-volum','create-snapshot','config-query'])
parser.add_argument('--instance-id', help='Use your command and --instance-id "your-instance-id" to get tags about the instance or make snapshot', metavar=' ID')
parser.add_argument('--bucket', help='Name of the S3 bucket to list objects in, get tags from or priv with priv-s3 command', metavar=' BUCKET')
parser.add_argument('--assume-role', action='store_true', help='Assume AWS IAM Role')
parser.add_argument('--volume-id', help='ID of the volume to create a snapshot for', metavar=' VOLUME_ID', required=False)
parser.add_argument('--query', help='Expressão de consulta para AWS Config')
parser.add_argument('--aggregator-name', help='Nome do Configuration Aggregator', required=True)
parser.add_argument('--search-ec2', help='Nome da instância EC2 para buscar')
parser.add_argument('--search-s3', help='Nome do bucket S3 para buscar')

args = parser.parse_args()


################################## ASSUME ROLE ##################################



def assumir_funcao(numero_conta, nome_role, nome_sessao):
    sts_client = boto3.client('sts')

    try:
        response = sts_client.assume_role(
            RoleArn=f'arn:aws:iam::{numero_conta}:role/{nome_role}',
            RoleSessionName=nome_sessao
        )

        print("Assumiu com sucesso a função. Detalhes da credencial:")
        print(f"AccessKeyId: {response['Credentials']['AccessKeyId']}")
        print(f"SecretAccessKey: {response['Credentials']['SecretAccessKey']}")
        print(f"SessionToken: {response['Credentials']['SessionToken']}")
    except Exception as e:
        print(f"Erro ao assumir a função: {e}")

if args.assume_role:
    numero_conta = input("Digite o número da conta: ")
    nome_role = input("Digite o nome da role: ")
    nome_sessao = input("Digite o nome da sessão: ")
    assumir_funcao(numero_conta, nome_role, nome_sessao)
    exit()


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

################################## AWS CONFIG ##################################

# Função para realizar a consulta no AWS Config

def get_config_results(query, aggregator_name):
    config_client = boto3.client('config',region_name='us-east-1')

    try:
        response = config_client.select_aggregate_resource_config(
            Expression=query,
            ConfigurationAggregatorName=aggregator_name,
        )

        results = response.get('Results', [])
        return results
    except Exception as e:
        print(f"Erro ao realizar a consulta: {e}")
        return []
 
if args.command == 'config-query':
    if args.search_ec2:
        query_expression = f'SELECT resourceId, resourceName, accountId, resourceType WHERE resourceType=\'AWS::EC2::Instance\' AND resourceId=\'{args.search_ec2}\''
    elif args.search_s3:
        query_expression = f'SELECT resourceId, resourceName, accountId, resourceType WHERE resourceType=\'AWS::S3::Bucket\' AND resourceId=\'{args.search_s3}\''
    elif args.query:
        query_expression = args.query
    else:
        print("Erro: Você deve fornecer o argumento --aggregator-name, --search-s3 ou --search-ec2 para o comando 'config-query'.")
        exit()

    results = get_config_results(query_expression, args.aggregator_name)
    
    
    if results:
        print("Resultados:")
        for result in results:
            print(result)
    else:
        print("Nenhum resultado encontrado.")
    
# if args.command == 'config-query':
#     if not args.query:
#         print("Erro: Você deve fornecer o argumento --query para o comando 'config-query'.")
#     else:
#         results = get_config_results(args.query, args.aggregator_name)
#         if results:
#             print("Resultados:")
#             for result in results:
#                 print(result)
#         else:
#             print("Nenhum resultado encontrado.")   

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



################################## EC2 ##################################

elif args.command == 'list-ec2':
    ec2 = boto3.client('ec2', region_name='us-east-1')

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


# Lista Volumes

elif args.command == 'list-volum':
    ec2 = boto3.client('ec2', region_name='us-east-1')

    # Lista os volumes EC2
    response_volumes = ec2.describe_volumes()

    print("EC2 Volumes:")
    for volume in response_volumes['Volumes']:
        print(f"Volume ID: {volume['VolumeId']}")
        print(f"Volume Type: {volume['VolumeType']}")
        print(f"Size: {volume['Size']} GiB")
        print(f"State: {volume['State']}")
        print(f"Instance: {volume['Attachments'][0]['InstanceId']}")
        print()


elif args.command == 'get-tags-ec2':
    if not args.instance_id:
        print("Error: You must provide the --instance-id argument for 'get-tags-ec2' command.")
    else:
        ec2 = boto3.client('ec2', region_name='us-east-1')

        # Obtém as tags da instância EC2 especificada
        try:
            response = ec2.describe_tags(Filters=[{'Name': 'resource-id', 'Values': [args.instance_id]}])

            print(f"Tags for EC2 Instance ID '{args.instance_id}':")
            for tag in response['Tags']:
                print(f"- {tag['Key']}: {tag['Value']}")
        except Exception as e:
            print(f"Error: {e}")


################# CRIAÇÃO DE SNAPSHOT DE VOLUME #################

elif args.command == 'create-snapshot':
    # Crie um cliente EC2
    ec2 = boto3.client('ec2', region_name='us-east-1')

    try:
        # Gere um timestamp único para o nome do snapshot
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

        # Se o ID do volume não foi fornecido como argumento, solicite ao usuário
        if not args.volume_id:
            args.volume_id = input("Digite o ID do volume: ")

        # Crie um snapshot do volume
        response = ec2.create_snapshot(
            VolumeId=args.volume_id,
            Description=f"Snapshot for volume {args.volume_id} at {timestamp}"
        )

        print(f"Snapshot created successfully. Snapshot ID: {response['SnapshotId']}")

    except Exception as e:
        print(f"Error creating snapshot: {e}")



    
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


def main():
    print("☁️   Informações da conta:")
    sts = boto3.client('sts')
    response = sts.get_caller_identity()

    print(f"User ID: {response['UserId']}")
    print(f"Account ID: {response['Account']}")
    print(f"ARN: {response['Arn']}")
    print()

def privar_bucket_s3(bucket_name):
    s3 = boto3.client('s3')

    try:
        # Cria uma nova política que torna o bucket privado
        bucket_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Deny",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*"
                }
            ]
        }

        # Converte a política para uma string JSON
        bucket_policy_json = json.dumps(bucket_policy)

        # Define a política no bucket
        s3.put_bucket_policy(
            Bucket=bucket_name,
            Policy=bucket_policy_json
        )

        print(f"O bucket {bucket_name} foi configurado como privado com sucesso.")
    except Exception as e:
        print(f"Erro ao configurar o bucket como privado: {e}")
        
if __name__ == "__main__":

    if args.command == 'info':
        main()
    elif args.command == 'priv-s3':
        if not args.bucket:
            print("Erro: Você deve fornecer o argumento --bucket para o comando 'priv-s3'.")
        else:
            privar_bucket_s3(args.bucket)
