#!/bin/bash

# Variáveis para o papel IAM e a sessão
ROLE_ARN="ARN_DO_SEU_PAPEL"
SESSION_NAME="NOME_DA_SESSAO"

# Nome do arquivo para armazenar a saída JSON
output_file="role_credentials.json"

# Assuma o papel IAM e redirecione a saída para um arquivo
aws sts assume-role --role-arn "$ROLE_ARN" --role-session-name "$SESSION_NAME" > "$output_file"

# Extraia as credenciais do arquivo
AWS_ACCESS_KEY_ID=$(cat "$output_file" | grep -o '"AccessKeyId": "[^"]*' | cut -d'"' -f4)
AWS_SECRET_ACCESS_KEY=$(cat "$output_file" | grep -o '"SecretAccessKey": "[^"]*' | cut -d'"' -f4)
AWS_SESSION_TOKEN=$(cat "$output_file" | grep -o '"SessionToken": "[^"]*' | cut -d'"' -f4)

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
# Por exemplo
