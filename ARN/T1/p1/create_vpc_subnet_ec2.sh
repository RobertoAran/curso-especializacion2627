#!/bin/bash
# Practica 1 - Creacion de VPC + subred + EC2 con AWS CLI
# sin Internet Gateway: la instancia no sera accesible desde el exterior.

export AWS_PAGER=""

# Variables globales
TAGENAME="aws2_10"
AMI_ID="ami-0ecb62995f68bb549"

echo "=== Start Deployment ==="

echo "Starting VPC..."
VPC_ID=$(aws ec2 create-vpc \
    --cidr-block 172.16.0.0/16 \
    --amazon-provided-ipv6-cidr-block \
    --tag-specifications "ResourceType=vpc,Tags=[{Key=Name,Value=$TAGENAME}]" \
    --query "Vpc.VpcId" \
    --output text)
echo "-> VPC created with ID: $VPC_ID"

aws ec2 modify-vpc-attribute \
    --vpc-id "$VPC_ID" \
    --enable-dns-hostnames "{\"Value\":true}"
echo "-> DNS hostnames enabled"

echo "Starting Subnet..."
SUB_ID=$(aws ec2 create-subnet \
    --vpc-id "$VPC_ID" \
    --cidr-block 172.16.1.0/24 \
    --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=$TAGENAME}]" \
    --query "Subnet.SubnetId" \
    --output text)
echo "-> Subnet created with ID: $SUB_ID"

aws ec2 modify-subnet-attribute \
    --subnet-id "$SUB_ID" \
    --map-public-ip-on-launch
echo "-> Public IP on launch enabled for: $SUB_ID"

echo "Starting Security Group..."
SG_ID=$(aws ec2 create-security-group \
    --vpc-id "$VPC_ID" \
    --group-name "gs-mio" \
    --description "my security group for port 22" \
    --tag-specifications "ResourceType=security-group,Tags=[{Key=Name,Value=$TAGENAME}]" \
    --query "GroupId" \
    --output text)
echo "-> Security Group created with ID: $SG_ID"

echo "Configuring Security Group to allow SSH access..."
RULE_ID=$(aws ec2 authorize-security-group-ingress \
    --group-id "$SG_ID" \
    --protocol tcp \
    --port 22 \
    --cidr 0.0.0.0/0 \
    --query "SecurityGroupRules[0].SecurityGroupRuleId" \
    --output text)
echo "-> Security Group rule created with ID: $RULE_ID"

echo "Launching EC2 Instance..."
EC2_ID=$(aws ec2 run-instances \
    --image-id "$AMI_ID" \
    --instance-type t3.micro \
    --key-name vockey \
    --subnet-id "$SUB_ID" \
    --security-group-ids "$SG_ID" \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$TAGENAME}]" \
    --query "Instances[0].InstanceId" \
    --output text)
echo "-> EC2 Instance launched with ID: $EC2_ID"

echo "Waiting for the instance to be running..."
aws ec2 wait instance-running --instance-ids "$EC2_ID"
aws ec2 describe-instances \
    --instance-ids "$EC2_ID" \
    --query "Reservations[0].Instances[0].[PublicIpAddress,PrivateIpAddress]" \
    --output text | while read PUB PRIV; do
        echo "-> Public IP:  $PUB"
        echo "-> Private IP: $PRIV"
    done

echo "=== Deployment Completed Successfully ==="
