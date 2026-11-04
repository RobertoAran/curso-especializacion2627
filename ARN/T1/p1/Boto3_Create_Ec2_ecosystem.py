import boto3

DRYRUN = False
AVALIABILITY_ZONE = 'us-east-1'

TAGNAMEVPC = 'vpcTestBoto3'

def create_vpc(ec2):
    vpc = ec2.create_vpc(
        CidrBlock='172.16.0.0/22',
        TagSpecifications=[
        {
            'ResourceType': 'vpc',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': TAGNAMEVPC
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
        CidrBlock='172.16.0.0/24',
        TagSpecifications=[
        {
            'ResourceType': 'subnet',
            'Tags': [
                {
                    'Key': 'Name',
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

def create_ec2instance(ec2, subnet_id):
    Ec2Instance = ec2.create_instances(
        ImageId = 'ami-0ecb62995f68bb549',
        InstanceType = 't3.micro',
        SubnetId = subnet_id,
        TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': 'Ec3InstanceTestBoto3'
                        },
                    ]
                },
                ],
        MaxCount = 1,
        MinCount = 1,
        DryRun = DRYRUN
    )
    ec2Instance_id = Ec2Instance[0].id
    print("Ec2Instance with id " + ec2Instance_id + " created correctly")
    return ec2Instance_id

if __name__ == "__main__":
    ec2client = boto3.client('ec2')
    ec2resource = boto3.resource('ec2')

    vpc_id = create_vpc(ec2client)
    print("VPC Creation process finished")
    subnet_id = create_subnets(ec2client, vpc_id)
    print("Subnet_id creation process finished")
    Ec2Instance_id = create_ec2instance(ec2resource, subnet_id)
    print("ec2 creation process finished")
