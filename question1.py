import boto3
import csv
from botocore.exceptions import BotoCoreError, ClientError

def get_regions(session):
    ec2 = session.client("ec2")
    try:
        return [r['RegionName'] for r in ec2.describe_regions()['Regions']]
    except (BotoCoreError, ClientError) as e:
        print(f"Error fetching regions: {e}")
        return []

def fetch_instance_types(session, region):
    ec2 = session.client("ec2", region_name=region)
    instance_types = set()

    try:
        paginator = ec2.get_paginator("describe_instance_types")
        for page in paginator.paginate():
            instance_types.update(i["InstanceType"] for i in page["InstanceTypes"])
    except (BotoCoreError, ClientError) as e:
        print(f"Failed to fetch instance types for {region}: {e}")

    return list(instance_types)

def save_csv(data, filename="ec2_instance_types.csv"):
    try:
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Region", "Instance Type"])
            writer.writerows(data)
        print(f"Data saved to {filename}")
    except IOError as e:
        print(f"Error writing to CSV file: {e}")

def main():
    session = boto3.Session(profile_name="default")
    regions = get_regions(session)
    records = []

    for region in regions:
        print(f"Processing region: {region}")
        types = fetch_instance_types(session, region)
        records.extend([[region, t] for t in types])

    save_csv(records)

if __name__ == "__main__":
    main()