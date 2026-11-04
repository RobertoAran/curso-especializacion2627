import boto3

#Code to delete VPC - SUBNETS 8163

#get the ec2Instance by tag
def get_ec2Instance_by_tag(ec2):
    ec2Instance_ids_array = []
    ec2Instance_id_raw = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    'Ec3InstanceTestBoto3'
                ]
            },
            {
                'Name': 'instance-state-name',
                'Values': ['pending', 'running', 'shutting-down', 'stopping', 'stopped']
            }
        ]
    )
    for reservation in ec2Instance_id_raw['Reservations']:
        for instance in reservation['Instances']:
            ec2Instance_ids_array.append(instance['InstanceId'])


    return ec2Instance_ids_array

#delete ec2Instance by ID
def delete_ec2Instance(ec2, ec2Instance_id):
    for instance_id in ec2Instance_id:
        ec2.terminate_instances(
            InstanceIds = [instance_id],
            DryRun = False
        )
        waiter = ec2.get_waiter('instance_terminated')
        print("Waiting for instance " + instance_id + " to be terminated...")
        waiter.wait(InstanceIds=[instance_id])
        print("Ec2Instance with id " + instance_id + " deleted correctly")

#Get subnet by tag
def get_subnet_by_tag(ec2):
    subnets_ids_array = []
    subnets_id_raw = ec2.describe_subnets(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    'subnetTestBoto3'
                ]
            },
        ]
    )
    for subnet in subnets_id_raw['Subnets']:
        subnets_ids_array.append(subnet['SubnetId'])


    return subnets_ids_array
#delete subnet by ID
def delete_subnets(ec2, subnets_id):
    for subnet_id in subnets_id:
        ec2.delete_subnet(
            SubnetId = subnet_id,
            DryRun = False
        )
        print("Subnet with id " + subnet_id + " deleted correctly")

#Get the vpc ID's by tags
def get_vpcs_tag(ec2):
    vpcs_ids_array = []
    vpcs_id_raw = ec2.describe_vpcs(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    'vpcTestBoto3'
                ]
            },
        ]
    )
    for vpc in vpcs_id_raw['Vpcs']:
        vpcs_ids_array.append(vpc['VpcId'])


    return vpcs_ids_array

#delete the vpc by ID
def delete_vpcs(ec2, vpcs_id):
    for vpc_id in vpcs_id:
        ec2.delete_vpc(
            VpcId = vpc_id,
            DryRun = False
        )
        print("VPC with id " + vpc_id + " deleted correctly")


if __name__ == "__main__":
    ec2 = boto3.client('ec2')

    ec2Instance_id = get_ec2Instance_by_tag(ec2)
    print(ec2Instance_id)
    delete_ec2Instance(ec2, ec2Instance_id)

    subnets_id = get_subnet_by_tag(ec2)
    print(subnets_id)
    delete_subnets(ec2, subnets_id)

    vpcs_id = get_vpcs_tag(ec2)
    print(vpcs_id)
    delete_vpcs(ec2, vpcs_id)