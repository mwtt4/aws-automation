print("EC2 Instances:")
for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        name = ''
        for tag in instance['Tags']:
            if tag['Key'] == 'Name':
                name = tag['Value']
        print(f"Instance Name: {name}")
        print(f"Instance ID: {instance['InstanceId']}")
        print(f"Instance Type: {instance['InstanceType']}")
        print(f"State: {instance['State']['Name']}")
        for interface in instance['NetworkInterfaces']:
            print(f"Private IP: {interface['PrivateIpAddress']}")
            print(f"Public IP: {interface.get('Association', {}).get('PublicIp', 'N/A')}")
            print(f"Elastic IP: {interface.get('Association', {}).get('PublicIp', 'N/A')}")
            print(f"VPC: {interface['VpcId']}")
        print(f"Launch Date: {instance['LaunchTime']}")
        print()
