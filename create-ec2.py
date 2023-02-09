# Pré-requisitos
# - Ter uma chave SSH criada na AWS
# - Criar uma lambda
#   - Permissões necessárias: Cloudwatch (Create Logs) e EC2:RunInstances
# Depois de importar o codigo, vou importar as variaveis na minha função lambda pela console da AWS

import os
import boto3

AMI = os.environ['AMI']
INSTANCE_TYPE = os.environ['INSTANCE_TYPE']
KEY_NAME = os.environ['KEY_NAME']
SUBNET_ID = os.environ['SUBNET_ID']

ec2 = boto3.resource('ec2')

def lambda_handler(event, context):
        instance = ec2.create_instance(
            ImageID=AMI,
            InstanceType=INSTANCE_TYPE,
            KeyName=KEY_NAME,
            SubnetId=SUBNET_ID,
            MaxCount=1,
            MinCount=1
        )

        print("New Instance Created: ", instance[0].id)