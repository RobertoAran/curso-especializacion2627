import boto3

DRYRUN = True

def create_ec2instance(ec2):
    ec2instance = ec2.create_instances(
        ImageId = 'ami-0d97d7f07b25dd693',
        InstanceType = 't3.micro',
        KeyName = 'vockey',
        BlockDeviceMappings=[
            {
                'Ebs': {
                    'VolumeSize': '10,0',
                    'VolumeType': 'gp3'
                },
            },
        ],
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Nane',
                        'Value': 'wp-web-xx'
                    },
                    {
                        'key': 'Proyecto',
                        'value': 'UD01'
                    },
                    {
                        'key': 'Propietario',
                        'value': 'Roberto Aranda'
                    },
                    {
                        'key': 'Rol',
                        'value': 'Web'
                    }                        
                ]
            },
        ],
        IamInstanceProfile={
        'Name': 'LabInstanceProfile'
        },        
        SecurityGroups=[
        'wp-web-sg',
        ],
        MaxCount = 1,
        MinCount = 1,
        DryRun = DRYRUN
    )

def create_elastic_and_assign():
    response = ec2.release_address(AllocationId='ALLOCATION_ID')
    print('Address released')

if __name__ == "__main__":
    ec2 = boto3.client('ec2')
    create_ec2instance(ec2)
    #create_elastic_and_assign()