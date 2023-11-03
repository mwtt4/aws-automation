# Execute o comando 'aws sts assume-role' e armazene a saída JSON em uma variável
role_credentials=$(aws sts assume-role --role-arn "ARN_DO_SEU_PAPEL" --role-session-name "NOME_DA_SESSAO")

# Extraia as credenciais da variável manualmente
AWS_ACCESS_KEY_ID=$(echo "$role_credentials" | grep -o '"AccessKeyId": "[^"]*' | cut -d'"' -f4)
AWS_SECRET_ACCESS_KEY=$(echo "$role_credentials" | grep -o '"SecretAccessKey": "[^"]*' | cut -d'"' -f4)
AWS_SESSION_TOKEN=$(echo "$role_credentials" | grep -o '"SessionToken": "[^"]*' | cut -d'"' -f4)

# Exporte as variáveis de ambiente
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY
export AWS_SESSION_TOKEN

# Agora você pode usar as variáveis de ambiente exportadas para autenticar suas chamadas da AWS
