import boto3

session = boto3.Session(profile_name="default", region_name="us-east-1")
client = session.client(service_name="ec2")

all_regions = client.describe_regions()


list_of_Regions = []

for each_reg in all_regions['Regions']:
  
    list_of_Regions.append(each_reg['RegionName'])

print(list_of_Regions)

for each_reg in list_of_Regions:
    session = boto3.Session(profile_name="default", region_name=each_reg)
    resource = session.resource(service_name="ec2")
    print("List of EC2 Instances from the region: ", each_reg)
    for each_in in resource.instances.all():
        print(each_in.id, each_in.state['Name'])
