#!/bin/bash

# Variáveis para o papel IAM e a sessão
ROLE_ARN="ARN_DO_SEU_PAPEL"
SESSION_NAME="NOME_DA_SESSAO"

# Assuma o papel IAM e armazene as credenciais temporárias nas variáveis de ambiente
role_credentials=$(aws sts assume-role --role-arn "$ROLE_ARN" --role-session-name "$SESSION_NAME")

export AWS_ACCESS_KEY_ID=$(echo $role_credentials | jq -r '.Credentials.AccessKeyId')
export AWS_SECRET_ACCESS_KEY=$(echo $role_credentials | jq -r '.Credentials.SecretAccessKey')
export AWS_SESSION_TOKEN=$(echo $role_credentials | jq -r '.Credentials.SessionToken')

# Configurar o perfil temporário no AWS CLI
aws configure --profile temporary_profile <<EOL
$AWS_ACCESS_KEY_ID
$AWS_SECRET_ACCESS_KEY
$AWS_SESSION_TOKEN
us-east-1 # Região da AWS (altere conforme necessário)
json # Formato de saída preferido (pode ser alterado)
EOL

echo "Perfil temporário 'temporary_profile' configurado."

# Você pode usar o perfil temporário para realizar operações na AWS
# Por exemplo:
# aws s3 ls --profile temporary_profile
