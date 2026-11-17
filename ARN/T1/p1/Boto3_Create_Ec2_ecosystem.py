import boto3

# Práctica 1 - Creación de VPC + subred + EC2 con boto3
# SIN Internet Gateway: la instancia NO será accesible desde el exterior.

# Global Variables
DRYRUN = False
TAGNAME = 'aws2_10'
AMI_ID = 'ami-0ecb62995f68bb549'
KEY_NAME = 'vockey'


def name_tags(resource_type):
    return [{
        'ResourceType': resource_type,
        'Tags': [{'Key': 'Name', 'Value': TAGNAME}]
    }]


def create_vpc(ec2):
    vpc = ec2.create_vpc(
        CidrBlock='172.16.0.0/16',
        AmazonProvidedIpv6CidrBlock=True,
        TagSpecifications=name_tags('vpc'),
        DryRun=DRYRUN
    )
    vpc_id = vpc['Vpc']['VpcId']
    ec2.get_waiter('vpc_available').wait(VpcIds=[vpc_id])
    print("VPC with id " + vpc_id + " created correctly")

    ec2.modify_vpc_attribute(
        VpcId=vpc_id,
        EnableDnsHostnames={'Value': True}
    )
    print("-> DNS hostnames enabled")
    return vpc_id


def create_subnet(ec2, vpc_id):
    subnet = ec2.create_subnet(
        VpcId=vpc_id,
        CidrBlock='172.16.1.0/24',
        TagSpecifications=name_tags('subnet'),
        DryRun=DRYRUN
    )
    subnet_id = subnet['Subnet']['SubnetId']
    print("Subnet with id " + subnet_id + " created correctly")

    ec2.modify_subnet_attribute(
        SubnetId=subnet_id,
        MapPublicIpOnLaunch={'Value': True}
    )
    print("-> Public IP on launch enabled")
    return subnet_id


def create_security_group(ec2, vpc_id):
    sg = ec2.create_security_group(
        GroupName='gs-mio',
        Description='my security group for port 22',
        VpcId=vpc_id,
        TagSpecifications=name_tags('security-group'),
        DryRun=DRYRUN
    )
    sg_id = sg['GroupId']
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[{
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }]
    )
    print("Security Group with id " + sg_id + " created (SSH allowed)")
    return sg_id


def create_ec2instance(ec2, subnet_id, sg_id):
    response = ec2.run_instances(
        ImageId=AMI_ID,
        InstanceType='t3.micro',
        KeyName=KEY_NAME,
        SubnetId=subnet_id,
        SecurityGroupIds=[sg_id],
        MinCount=1,
        MaxCount=1,
        TagSpecifications=name_tags('instance'),
        DryRun=DRYRUN
    )
    instance_id = response['Instances'][0]['InstanceId']
    print("Ec2Instance with id " + instance_id + " launched, waiting until running...")

    ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])
    instance = ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
    public_ip = instance.get('PublicIpAddress')
    print("-> Public IP:  " + str(public_ip))
    print("-> Private IP: " + str(instance.get('PrivateIpAddress')))
    print("-> Try: ssh -i labsuser.pem ubuntu@" + str(public_ip) + "  (debería FALLAR: no hay IGW)")
    return instance_id


if __name__ == "__main__":
    ec2 = boto3.client('ec2')

    vpc_id = create_vpc(ec2)
    subnet_id = create_subnet(ec2, vpc_id)
    sg_id = create_security_group(ec2, vpc_id)
    create_ec2instance(ec2, subnet_id, sg_id)

    print("=== Deployment Completed Successfully ===")
