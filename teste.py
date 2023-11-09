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
