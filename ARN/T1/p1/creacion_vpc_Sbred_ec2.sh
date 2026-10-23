#!/usr/bin/env bash
##TODO
#Crear vpc
#crear Subred
#Crear Ec2


#Cosas creadas
##VPC
##Grupo de seguridad
##ec2

#para la subnet necesitamos 
##1 subred
##0 privadas
##cidr subred publica = 172.16.0.0/20

SG_ID$


#Creamos vpc
VPC_ID=$(aws ec2 create-vpc \
    --cidr-block 172.16.0.0/16 \
    --amazon-provider-ipv6-cidr-block \
    --tag-specifications 'ResourceType=vpc, Tags=[{Key=Name, Value=mivpc}]' \
    --query "VpcId" \
    --output text)


SUB_ID=$(aws ec2 create-subnet \
    --vpc-id vpc-081ec835f3EXAMPLE \
    --cidr-block 10.0.0.0/24 \
    --tag-specifications ResourceType=subnet,Tags=[{Key=Name,Value=miSubnet}] \
    --query "SubnetId" --output text)

SG_ID=$(aws ec2 create-security-group --vpc-id $VPC_ID \
    --group-name gs-mio \
    --description "Mi grupo de seguridad para habrir el puerto 22" \
    --query GroupId --output text)

aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --ip-permissions '[{"IpProtocol": "tcp", "FromPort": 22, "ToPort": 22, "IpRange": [{"CidrIp": "0.0.0.0"}]}]'

aws ec2 create-tags \
    --Reources $SG_ID \
    --tags "key=Name,Value=migruposeguridad"

EC2_ID=$(aws ec2 run-instances \
    --image-id ami-0ecb62995f68bb549 \
    --instance-type t3.micro \
    --key-name vockey \
    --subnet-id $SUB_ID \
    --security-group-ids $SG_ID \
    --associate-public-ip-address \
    --tag-specifications 'ResourceType=instance, Tags=[{Key=Name, Value=miec2}]') \
    --query Instances.InstanceId --output text