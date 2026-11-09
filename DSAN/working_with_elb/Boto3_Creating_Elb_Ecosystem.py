import boto3

DRYRUN = False
AVALIABILITY_ZONE = 'us-east-1'

TAGNAMEVPC = 'CreatingElbBoto3'


def create_security_group(ec2, vpc_id):
    security_group = ec2.create_security_group(
        GroupName='CreatingElbBoto3',
        Description='Security group for CreatingElbBoto3',
        VpcId=vpc_id,
        TagSpecifications=[
            {
                'ResourceType': 'security-group',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'CreatingElbBoto3'
                    },
                ]
            },
        DryRun=DRYRUN
    )
    security_group_id = security_group['GroupId']
    print("Security Group with id " + security_group_id + " created correctly")
    return security_group_id



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