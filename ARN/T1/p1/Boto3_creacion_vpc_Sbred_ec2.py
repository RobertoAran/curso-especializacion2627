import boto3

DRYRUN = True

def crear_vpc():
    ec2 = boto3.client('ec2')


    vpc = ec2.create_vpc(
        CidrBlock='172.16.0.0/16',
        TagSpecifications=[
        {
            'ResourceType': 'vpc',
            'Tags': [
                {
                    'Key': 'Nane',
                    'Value': 'testVPC'
                },
            ]
        },
        ],
        AmazonProvidedIpv6CidrBlock=True,
        DryRun=DRYRUN
    )

    vpc_id = vpc['VPC']['VpcId']

    printf("Se ha creado la vpc con id " vpc_id " correctamente3")

    ec2.modify_vpc_attribute

    ## falta habilitar dns support, hostnames
    #segundo creamos la subnet

    #tercero creamos la ec2 asociado a la vpc y la subnet


if __name__ == "__main__":
    crear_vpc()