import boto3

# Replace with your AWS access key ID and secret access key
access_key = "YOUR_ACCESS_KEY_ID"
secret_key = "YOUR_SECRET_ACCESS_KEY"

# Create an EC2 client
ec2 = boto3.client('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key)

# Create a security group
response = ec2.create_security_group(
    GroupName='my-security-group',
    Description='A security group for my web application'
)

security_group_id = response['GroupId']

# Add an inbound rule to allow HTTP traffic from anywhere
response = ec2.authorize_security_group_ingress(
    GroupId=security_group_id,
    IpProtocol='tcp',
    FromPort=80,
    ToPort=80,
    CidrIp='0.0.0.0/0'
)

# Create an EC2 instance
response = ec2.run_instances(
    ImageId='ami-0c55b159cbfafe1f0',  # Replace with your desired AMI ID
    MinCount=1,
    MaxCount=1,
    KeyName='your-key-pair-name',  # Replace with your key pair name
    SecurityGroupIds=[security_group_id]
)

instance_id = response['Instances'][0]['InstanceId']

# Wait for the instance to start
waiter = ec2.get_waiter('instance_running')
waiter.wait(InstanceIds=[instance_id])

# Get the public IP address of the instance
response = ec2.describe_instances(InstanceIds=[instance_id])
public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']

print("Your web application is running at:", public_ip)