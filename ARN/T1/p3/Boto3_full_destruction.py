import boto3

# Code to delete EC2 - SG - IGW - SUBNETS - ROUTE TABLES - VPC

# Global Variables
TAGNAME = "aws2_12"


def tag_filter():
    return [{'Name': 'tag:Name', 'Values': [TAGNAME]}]


# ---------- EC2 ----------
def get_ec2Instance_by_tag(ec2):
    ids = []
    response = ec2.describe_instances(
        Filters=tag_filter() + [{
            'Name': 'instance-state-name',
            'Values': ['pending', 'running', 'shutting-down', 'stopping', 'stopped']
        }]
    )
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            ids.append(instance['InstanceId'])
    return ids


def delete_ec2Instances(ec2, instance_ids):
    if not instance_ids:
        return
    ec2.terminate_instances(InstanceIds=instance_ids)
    print("Waiting for instances " + str(instance_ids) + " to be terminated...")
    ec2.get_waiter('instance_terminated').wait(InstanceIds=instance_ids)
    for instance_id in instance_ids:
        print("Ec2Instance with id " + instance_id + " deleted correctly")


# ---------- SECURITY GROUPS ----------
def get_sg_by_tag(ec2):
    response = ec2.describe_security_groups(Filters=tag_filter())
    return [sg['GroupId'] for sg in response['SecurityGroups']]


def delete_sgs(ec2, sg_ids):
    for sg_id in sg_ids:
        ec2.delete_security_group(GroupId=sg_id)
        print("Security Group with id " + sg_id + " deleted correctly")


# ---------- INTERNET GATEWAYS ----------
def get_igw_by_tag(ec2):
    response = ec2.describe_internet_gateways(Filters=tag_filter())
    return response['InternetGateways']

def delete_igws(ec2, igws):
    for igw in igws:
        igw_id = igw['InternetGatewayId']
        for attachment in igw.get('Attachments', []):
            ec2.detach_internet_gateway(
                InternetGatewayId=igw_id,
                VpcId=attachment['VpcId']
            )
            print("Internet Gateway " + igw_id + " detached from " + attachment['VpcId'])
        ec2.delete_internet_gateway(InternetGatewayId=igw_id)
        print("Internet Gateway with id " + igw_id + " deleted correctly")


# ---------- Elastic IPs ----------
def get_eip_by_tag(ec2):
    response = ec2.describe_addresses(Filters=tag_filter())
    return [eip['AllocationId'] for eip in response['Addresses']]

def delete_eips(ec2, allocation_ids):
    for allocation_id in allocation_ids:
        ec2.release_address(AllocationId=allocation_id)
        print("Elastic IP with allocation id " + allocation_id + " released correctly")


# --------- NAT GATEWAYS ----------
def get_nat_gateways_by_tag(ec2):
    response = ec2.describe_nat_gateways(Filters=tag_filter())
    return [nat['NatGatewayId'] for nat in response['NatGateways']]

def delete_nat_gateways(ec2, nat_gateway_ids):
    for nat_gateway_id in nat_gateway_ids:
        ec2.delete_nat_gateway(NatGatewayId=nat_gateway_id)
        print("NAT Gateway with id " + nat_gateway_id + " deleted correctly")


# ---------- SUBNETS ----------
def get_subnet_by_tag(ec2):
    response = ec2.describe_subnets(Filters=tag_filter())
    return [subnet['SubnetId'] for subnet in response['Subnets']]


def delete_subnets(ec2, subnet_ids):
    for subnet_id in subnet_ids:
        ec2.delete_subnet(SubnetId=subnet_id)
        print("Subnet with id " + subnet_id + " deleted correctly")


# ---------- ROUTE TABLES ----------
def get_route_tables_by_tag(ec2):
    response = ec2.describe_route_tables(Filters=tag_filter())
    return response['RouteTables']


def delete_route_tables(ec2, route_tables):
    for rt in route_tables:
        rt_id = rt['RouteTableId']
        # la tabla principal se borra sola con la VPC
        if any(assoc.get('Main') for assoc in rt.get('Associations', [])):
            continue
        for assoc in rt.get('Associations', []):
            ec2.disassociate_route_table(AssociationId=assoc['RouteTableAssociationId'])
        ec2.delete_route_table(RouteTableId=rt_id)
        print("Route table with id " + rt_id + " deleted correctly")


# ---------- VPC ----------
def get_vpcs_by_tag(ec2):
    response = ec2.describe_vpcs(Filters=tag_filter())
    return [vpc['VpcId'] for vpc in response['Vpcs']]


def delete_vpcs(ec2, vpc_ids):
    for vpc_id in vpc_ids:
        ec2.delete_vpc(VpcId=vpc_id)
        print("VPC with id " + vpc_id + " deleted correctly")


if __name__ == "__main__":
    ec2 = boto3.client('ec2')

    # El orden importa: primero lo que depende de otros recursos
    delete_ec2Instances(ec2, get_ec2Instance_by_tag(ec2))
    delete_sgs(ec2, get_sg_by_tag(ec2))
    delete_igws(ec2, get_igw_by_tag(ec2))
    delete_subnets(ec2, get_subnet_by_tag(ec2))
    delete_route_tables(ec2, get_route_tables_by_tag(ec2))
    delete_vpcs(ec2, get_vpcs_by_tag(ec2))

    print("=== Cleanup Completed Successfully ===")
