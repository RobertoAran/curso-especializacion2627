import boto3

DRYRUN = False

def create_vpc(ec2):
    vpc = ec2.create_vpc(
        CidrBlock='172.16.0.0/22',
        TagSpecifications=[
        {
            'ResourceType': 'vpc',
            'Tags': [
                {
                    'Key': 'Nane',
                    'Value': 'vpcTestBoto3'
                },
            ]
        },
        ],
        AmazonProvidedIpv6CidrBlock=True,
        DryRun=DRYRUN
    )
    vpc_id = vpc['Vpc']['VpcId']
    print("VPC With id " + vpc_id + " created correctly")

    ec2.modify_vpc_attribute(
        VpcId = vpc_id,
        EnableDnsHostnames={ 'Value': True },
    )
    print("DNS Activated")

    return vpc_id


def create_subnets(ec2, vpc_id):

    subnet = ec2.create_subnet(
        VpcId = vpc_id,
        CidrBlock='10.0.0.0/24',
        TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Nane',
                    'Value': 'subnetTestBoto3'
                },
            ]
        },
        ],
        DryRun = DRYRUN
    )
    subnet_id = subnet['Subnet']['SubnetId']
    print("Subnet with id " + subnet_id + " created correctly")

    return subnet_id

def create_ec2instance(ec2, vpc_id, subnet_id):
    Ec2Instance = ec2.create_instances(
        ImageId = 'ami-0ecb62995f68bb549',
        InstanceType = 't3.micro',
        VpcId = vpc_id,
        SubnetId = subnet_id,
        TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Nane',
                            'Value': 'Ec3InstanceTestBoto3'
                        },
                    ]
                },
                ],
        MaxCount = 1,
        MinCount = 1,
        DryRun = DRYRUN
    )
    ec2Instance_id = Ec2Instance['Subnet']['SubnetId']
    return Ec2Instance_id

if __name__ == "__main__":
    ec2 = boto3.client('ec2')

    vpc_id = create_vpc(ec2)
    print = "VPC Creation process finished"
    subnet_id = create_subnets(ec2, vpc_id)
    print = "Subnet_id creation process finished"
    Ec2Instance_id = create_ec2instance(ec2, vpc_id, subnet_id)
    print = "ec2 creation process finished"
