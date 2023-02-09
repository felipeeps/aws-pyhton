# Filtros -> Instancias com a tag backup=true
# Associar as permissões de EC2 Snapshot e CLoudwatch, na role utilizada

from datetime import datetime

import boto3

def lambda_handler(event, context):
    #Listando Regiões
    ec2_client = boto3.client('ec2')
    regions = [region['RegionName']
                for region in ec2_client.describe_regions()['Regions']]
    
    for region in regions:
        print('Instances in EC2 Region {0}:'.format(region))
        ec2 = boto3.resource('ec2', region_name=region)

        instances = ec2.instances.filter(
            Filters=[
                {'Name': 'tag:backup', 'Values': ['true']}
            ]
        )

        # Adicionando timestamp no snapshot, para controlar os mais recentes
        timestamp = datetime.utcnow().replace(microsecond=0).isoformat()

        for i in instances.all():
            for v in i.voluemes.all():
                desc = 'Backup of {0}, volume {1}, created {2}'.format(
                    i.id, v.id, timestamp)
                print(desc)
                
                snapshot = v.create_snapshot(Description=desc)

                print("Created snapshot:", snapshot.id)

# Para fazer o agendamento, no cloudwatch -> Events -> Rules
# Defino a frequencia que ele vai rodar e adiciono um target -> Função lambda