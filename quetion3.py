import boto3
from datetime import datetime

def get_billed_regions():
    ce = boto3.client('ce')
    today = datetime.today().strftime('%Y-%m-%d')

    try:
        response = ce.get_cost_and_usage(
            TimePeriod={'Start': '2025-01-01', 'End': '2025-02-15'},
            Granularity='MONTHLY',
            Metrics=['UnblendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'REGION'}]
        )

        regions = set()
        for time_period in response['ResultsByTime']:
            for group in time_period.get('Groups', []):
                if float(group['Metrics']['UnblendedCost']['Amount']) > 0:
                    regions.add(group['Keys'][0])

        return list(regions)

    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    regions = get_billed_regions()
    print("Billed regions:", regions if regions else "No billing records found.")
