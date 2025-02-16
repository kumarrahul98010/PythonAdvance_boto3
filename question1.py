import boto3
import csv

def get_regions():
    session = boto3.Session(profile_name="default")
    ec2 = session.client("ec2")
    return [r['RegionName'] for r in ec2.describe_regions()['Regions']]

def fetch_instance_types(region):
    session = boto3.Session(profile_name="default", region_name=region)
    ec2 = session.client("ec2")
    instance_types = set()

    paginator = ec2.get_paginator("describe_instance_types")
    for page in paginator.paginate():
        instance_types.update(i["InstanceType"] for i in page["InstanceTypes"])

    return list(instance_types)

def save_csv(data, filename="ec2_instance_types.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Region", "Instance Type"])
        writer.writerows(data)

def main():
    regions = get_regions()
    records = []

    for region in regions:
        try:
            types = fetch_instance_types(region)
            records.extend([[region, t] for t in types])
        except Exception as e:
            print(f"Failed to fetch data for {region}: {e}")

    save_csv(records)
    print("Saved EC2 instance types in ec2_instance_types.csv")

if __name__ == "__main__":
    main()
