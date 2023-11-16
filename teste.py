import argparse
import boto3
import json
import sys
import os
from colorama import init, Fore
from datetime import datetime

#SALVAR RESULTADO 
# def salvar_resultados(resultado, pasta):
#     try:
#         os.makedirs(pasta, exist_ok=True)
#         with open(os.path.join(pasta, 'resultados.txt'), 'w') as file:
#             file.write(resultado)
#         print(f"Resultados salvos em: {os.path.abspath(pasta)}")
#     except Exception as e:
#         print(f"Erro ao salvar os resultados: {e}")

# def main():
#     # Seção para obter a resposta do usuário
#     resposta_usuario = input("Deseja salvar as informações dos resultados? (s/n): ").lower()

#     # Se o usuário desejar salvar os resultados
#     if resposta_usuario == 's':
#         # Cria uma pasta com a data atual e o horário
#         pasta_resultados = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     else:
#         # Se o usuário não quiser salvar, a pasta será vazia
#         pasta_resultados = ''

#     # Restante do código principal
#     # ...

#     # Exemplo de como usar a função salvar_resultados
#     # Substitua 'resultado' pelo que você deseja salvar e 'pasta_resultados' pela variável usada no seu script
#     salvar_resultados('resultado', pasta_resultados)

# if __name__ == "__main__":
#     main()
 
class CustomFormatter(argparse.HelpFormatter):
    def _format_action(self, action):
        if action.nargs == 0:
            # Adicione um espaçamento maior entre as opções e descrições
            return super()._format_action(action) + '\n\n'
        return super()._format_action(action)
    

    
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



    
parser = argparse.ArgumentParser(description="",
        usage='use "%(prog)s --help" for more information',
        formatter_class=CustomFormatter)  # Use a classe de formatação personalizada

# Adicione descritivos aos comandos posicionais
commands_help = {
    'list-s3': 'List S3 buckets',
    'list-objects': 'List objects in an S3 bucket',
    'get-tags-s3': 'Get tags for an S3 bucket',
    'list-ec2': 'List EC2 instances',
    'get-tags-ec2': 'Get tags for an EC2 instance',
    'list-roles': 'List IAM roles',
    'list-eks': 'List Amazon EKS clusters',
    'list-cloudfront': 'List CloudFront distributions',
    'list-route53': 'List Route 53 hosted zones',
    'info': 'Display general information',
    'priv-s3': 'Make an S3 bucket private',
}

subparsers = parser.add_subparsers(title='positional arguments', dest='command')

for command, help_text in commands_help.items():
    subparser = subparsers.add_parser(command, help=help_text)

# Adicione espaçamento entre colunas usando a função add_argument
parser.add_argument('--instance-id', help='Use your command and --instance-id "your-instance-id" to get tags about the instance or make snapshot', metavar=' ID')
parser.add_argument('--bucket', help='Name of the S3 bucket to list objects in, get tags from or priv with priv-s3 command', metavar=' BUCKET')
parser.add_argument('--assume-role', action='store_true', help='Assume AWS IAM Role')

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


################################## AWS CONFIG ##################################



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

elif args.command == 'create-snapshot':
    if not args.instance_id:
        print("Error: You must provide the --instance-id argument for 'create-snapshot' command.")
    else:
        ec2 = boto3.client('ec2')
        try:
            # Gere um timestamp único para o nome do snapshot
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            
            # Crie um snapshot da instância EC2
            response = ec2.create_snapshot(
                VolumeId=args.instance_id,
                Description=f"Snapshot for instance {args.instance_id} at {timestamp}"
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

# ... (seu código existente)

def main():
    # Coloque o código principal aqui
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

