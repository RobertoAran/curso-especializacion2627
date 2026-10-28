import boto3

#Code to delete VPC - SUBNETS 8163

#Taking the vpc ID's (tags)
def get_vpcs_id(ec2):
    vpcs_ids_array = []
    vpcs_id_raw = ec2.describe_vpcs(
        Filters=[
            {
                'Name': 'tag:Nane',
                'Values': [
                    'vpcTestBoto3'
                ]
            },
        ]
    )
    for vpc in vpcs_id_raw['Vpcs']:
        vpcs_ids_array.append(vpc['VpcId'])


    return vpcs_ids_array





if __name__ == "__main__":
    ec2 = boto3.client('ec2')

    vpcs_id = get_vpcs_id(ec2)
    print(vpcs_id)